from typing import Optional, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from data.asyncl.mysql_data import init_setup
from data.asyncl.mysql_orm import DbQAgentServer
from grpc_client import GrpcQAgentConfig, GrpcQAgentClient
from grpc_protos.protos import dockermsg_pb2_grpc, dockermsg_pb2
from utils import StrUtil
from utils.jwt_auth import get_current_user
from web import resp_ok, resp_fail

router = APIRouter(tags=["QAgentServer client"])


class ImagesPull(BaseModel):
    repo_tag: str
    login_url: str
    username: Optional[str] = None
    password: Optional[str] = None


@router.get("/images/{id}")
async def images(
    id: int,
    name: Optional[str] = None,
    db: AsyncSession = Depends(init_setup.get_async_db),
    current_user: dict = Depends(get_current_user)
):
    sql = select(DbQAgentServer).filter(DbQAgentServer.id == id)
    qb = await db.execute(sql)
    row = qb.scalar_one_or_none()
    if StrUtil.is_none(row):
        return resp_fail(msg='找不到服务')
    qagent_config = GrpcQAgentConfig(host=row.host, port=row.port)
    datas = []
    with GrpcQAgentClient(qagent_config) as client:
        stub = dockermsg_pb2_grpc.DockerAgentStub(client.channel)
        request = dockermsg_pb2.Req_DockerImages(name=name if StrUtil.is_not_none(name) else None)
        response = stub.images(request)
        if response.code == 0:
            for im in response.images:
                datas.append({
                    'server_id': row.id,
                    'server_name': row.name,
                    'server_host': row.host,
                    'repository': im.repository,
                    'tag': im.tag,
                    'image_id': im.image_id,
                    'created': im.created,
                    'size': im.size,
                })
    return resp_ok(data=datas)


@router.get("/images_pull/{id}")
async def image_pull(
    id: int,
    image_pull: ImagesPull = Depends(),
    db: AsyncSession = Depends(init_setup.get_async_db),
    current_user: dict = Depends(get_current_user)
):
    if StrUtil.is_blank(image_pull.repo_tag) or StrUtil.is_blank(image_pull.login_url):
        return resp_fail(msg='缺失镜像tag或镜像地址')
    sql = select(DbQAgentServer).filter(DbQAgentServer.id == id)
    qb = await db.execute(sql)
    row = qb.scalar_one_or_none()
    if StrUtil.is_none(row):
        return resp_fail(msg='找不到服务')
    qagent_config = GrpcQAgentConfig(host=row.host, port=row.port)
    with GrpcQAgentClient(qagent_config) as client:
        stub = dockermsg_pb2_grpc.DockerAgentStub(client.channel)
        request = dockermsg_pb2.Req_DockerPull(**image_pull.dict())
        response = stub.pull_images(request)

    return resp_ok(msg=response.msg) if response.code == 0 else resp_fail(msg=response.msg)

