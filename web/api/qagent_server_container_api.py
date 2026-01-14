import logging
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application_config import random_token
from data.asyncl.mysql_data import init_setup
from data.asyncl.mysql_orm import DbQAgentContainer, DbQAgentServer
from grpc_client import GrpcQAgentConfig, GrpcQAgentClient
from grpc_protos.protos import dockermsg_pb2_grpc, dockermsg_pb2
from utils import StrUtil
from utils.jwt_auth import get_current_user
from web import resp_ok, resp_fail

router = APIRouter(tags=["QAgentServer container"])


logger = logging.getLogger(__name__)


class ContainerQueryList(BaseModel):
    container_name: Optional[str] = None
    images_id: Optional[str] = None
    server_id: Optional[int] = None
    ports: Optional[str] = None


class ImagesPull(BaseModel):
    repo_tag: str
    login_url: str
    username: Optional[str] = None
    password: Optional[str] = None


@router.get("/list")
async def querylist(
    query: ContainerQueryList = Depends(),
    db: AsyncSession = Depends(init_setup.get_async_db),
    current_user: dict = Depends(get_current_user)
):
    sql = select(DbQAgentContainer)
    if StrUtil.is_not_blank(query.container_name):
        sql.filter(DbQAgentContainer.container_name.like(f'{query.container_name}%'))
    if StrUtil.is_not_blank(query.images_id):
        sql.filter(DbQAgentContainer.images_id.like(f'{query.images_id}%'))
    if StrUtil.is_not_blank(query.ports):
        sql.filter(DbQAgentContainer.ports.like(f'{query.ports}%'))
    if StrUtil.is_not_none(query.server_id):
        sql.filter(DbQAgentContainer.server_id == query.server_id)
    qb = await db.execute(sql)
    rows = qb.scalars().all()
    return resp_ok(data=rows)


@router.post("/sync")
async def asyncinfos(
    token: str,
    db: AsyncSession = Depends(init_setup.get_async_db)
):
    if token != random_token:
        return resp_fail(msg='非法请求')
    sql = select(DbQAgentServer)
    qb = await db.execute(sql)
    rows = qb.scalars().all()
    logger.info(f'查询到服务器引擎:{rows}')
    if len(rows) > 0:
        for row in rows:
            if row.status != 1:
                continue
            try:
                qagent_config = GrpcQAgentConfig(host=row.host, port=row.port)
                data_rows = []
                with GrpcQAgentClient(qagent_config) as client:
                    stub = dockermsg_pb2_grpc.DockerAgentStub(client.channel)
                    request = dockermsg_pb2.Req_DockerInfo()
                    response = stub.container_info(request)
                    logger.info(f'查询到服务器：{qagent_config}，容器如下:{response}')
                    if response.code == 0:
                        infos = response.infos
                        for info in infos:
                            work_path = None
                            ll = info.labels.split(',')
                            for l in ll:
                                if l.startswith('com.docker.compose.project.working_dir='):
                                    work_path = l.replace('com.docker.compose.project.working_dir=', '')
                            d = {
                                'server_id': row.id,
                                'container_id': info.id,
                                'container_name': info.names,
                                'work_path': work_path,
                                'command': info.command,
                                'created_at': info.created_at,
                                'image': info.image,
                                'names': info.names,
                                'labels': info.labels,
                                'ports': info.ports,
                                'running_for': info.running_for,
                                'state': info.state,
                                'status': info.status,
                                'size': info.size
                            }
                            data_rows.append(d)
                        if len(data_rows) > 0:
                            for ii in data_rows:
                                query_sql = select(DbQAgentContainer).filter(
                                    DbQAgentContainer.container_name == ii.get('container_name', None))
                                query_qb = await db.execute(query_sql)
                                query_row = query_qb.scalar_one_or_none()
                                if StrUtil.is_none(query_row):
                                    new_data = DbQAgentContainer()
                                    for key, value in ii.items():
                                        if hasattr(new_data, key):
                                            setattr(new_data, key, value)
                                    db.add(new_data)
                                    await db.commit()
                                    await db.refresh(new_data)
                                else:
                                    for key, value in ii.items():
                                        if hasattr(query_row, key):
                                            setattr(query_row, key, value)
                                    await db.commit()
                                    await db.refresh(query_row)
                                logger.info(f'同步服务器：{qagent_config}，容器:{query_row}')
            except Exception as e:
                logger.error(f'同步服务QAgentServer容器错误', exc_info=True)
    return resp_ok()


@router.post("/rollback/{id}")
async def rollback(
    id: int,
    image_pull: ImagesPull = Depends(),
    db: AsyncSession = Depends(init_setup.get_async_db),
    current_user: dict = Depends(get_current_user)
):
    if StrUtil.is_blank(image_pull.repo_tag) or StrUtil.is_blank(image_pull.login_url):
        return resp_fail(msg='缺失镜像标签')
    sql = select(DbQAgentContainer).filter(DbQAgentContainer.id == id)
    qb = await db.execute(sql)
    row = qb.scalar_one_or_none()
    if StrUtil.is_none(row) or StrUtil.is_none(row.server_id):
        return resp_fail(msg='找不到容器')
    qagent_config = await query_server_config(row.server_id, db)
    with GrpcQAgentClient(qagent_config) as client:
        stub = dockermsg_pb2_grpc.DockerAgentStub(client.channel)
        request = dockermsg_pb2.Req_DockerRollBack(**{
            "container_id": row.container_id,
            "container_name": row.container_name,
            "work_path": row.work_path,
            "images_name": image_pull.repo_tag
        })
    response = stub.pull_images(request)
    return resp_ok(msg=response.msg) if response.code == 0 else resp_fail(msg=response.msg)


@router.post("/up/{id}")
async def up(
    id: int,
    db: AsyncSession = Depends(init_setup.get_async_db),
    current_user: dict = Depends(get_current_user)
):
    sql = select(DbQAgentContainer).filter(DbQAgentContainer.id == id)
    qb = await db.execute(sql)
    row = qb.scalar_one_or_none()
    if StrUtil.is_none(row) or StrUtil.is_none(row.server_id):
        return resp_fail(msg='找不到容器')
    qagent_config = await query_server_config(row.server_id, db)
    with GrpcQAgentClient(qagent_config) as client:
        stub = dockermsg_pb2_grpc.DockerAgentStub(client.channel)
        request = dockermsg_pb2.Req_DockerUp(**{
            "container_id": row.container_id,
            "container_name": row.container_name,
            "work_path": row.work_path,
        })
    response = stub.pull_images(request)
    return resp_ok(msg=response.msg) if response.code == 0 else resp_fail(msg=response.msg)



@router.post("/down/{id}")
async def down(
    id: int,
    db: AsyncSession = Depends(init_setup.get_async_db),
    current_user: dict = Depends(get_current_user)
):
    sql = select(DbQAgentContainer).filter(DbQAgentContainer.id == id)
    qb = await db.execute(sql)
    row = qb.scalar_one_or_none()
    if StrUtil.is_none(row) or StrUtil.is_none(row.server_id):
        return resp_fail(msg='找不到容器')
    qagent_config = await query_server_config(row.server_id, db)
    with GrpcQAgentClient(qagent_config) as client:
        stub = dockermsg_pb2_grpc.DockerAgentStub(client.channel)
        request = dockermsg_pb2.Req_DockerDown(**{
            "container_id": row.container_id,
            "container_name": row.container_name,
            "work_path": row.work_path,
        })
    response = stub.pull_images(request)
    return resp_ok(msg=response.msg) if response.code == 0 else resp_fail(msg=response.msg)


@router.post("/restart/{id}")
async def restart(
    id: int,
    db: AsyncSession = Depends(init_setup.get_async_db),
    current_user: dict = Depends(get_current_user)
):
    sql = select(DbQAgentContainer).filter(DbQAgentContainer.id == id)
    qb = await db.execute(sql)
    row = qb.scalar_one_or_none()
    if StrUtil.is_none(row) or StrUtil.is_none(row.server_id):
        return resp_fail(msg='找不到容器')
    qagent_config = await query_server_config(row.server_id, db)
    with GrpcQAgentClient(qagent_config) as client:
        stub = dockermsg_pb2_grpc.DockerAgentStub(client.channel)
        request = dockermsg_pb2.Req_DockerRestart(**{
            "container_id": row.container_id,
            "container_name": row.container_name,
            "work_path": row.work_path,
        })
    response = stub.pull_images(request)
    return resp_ok(msg=response.msg) if response.code == 0 else resp_fail(msg=response.msg)


async def query_server_config(id, db):
    sql = select(DbQAgentServer).filter(DbQAgentServer.id == id)
    qb = await db.execute(sql)
    row = qb.scalar_one_or_none()
    if StrUtil.is_none(row):
        return None
    qagent_config = GrpcQAgentConfig(host=row.host, port=row.port)
    return qagent_config
