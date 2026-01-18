from typing import Optional, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data.asyncl.mysql_data import init_setup
from data.asyncl.mysql_orm import DbQAgentServer
from utils import StrUtil
from utils.jwt_auth import get_current_user
from web import resp_ok, resp_fail

router = APIRouter(tags=["QAgentServer"])


class QAgentQueryList(BaseModel):
    name: Optional[str] = None
    host: Optional[str] = None
    status: Optional[int] = None


class AddQAgent(BaseModel):
    name: str = None
    host: Optional[str] = 'localhost'
    port: Optional[int] = 6305
    status: Optional[int] = 1


class PutQAgent(BaseModel):
    id: int
    name: str
    host: str
    port: int
    status: int


@router.get("/list")
async def querylist(
    query: QAgentQueryList = Depends(),
    db: AsyncSession = Depends(init_setup.get_async_db),
    current_user: dict = Depends(get_current_user)
):
    sql = select(DbQAgentServer)
    if StrUtil.is_not_blank(query.name):
        sql = sql.filter(DbQAgentServer.name.like(f'{query.name}%'))
    if StrUtil.is_not_blank(query.host):
        sql = sql.filter(DbQAgentServer.host.like(f'{query.host}%'))
    if StrUtil.is_not_none(query.status):
        sql = sql.filter(DbQAgentServer.status == query.status)
    qb = await db.execute(sql)
    rows = qb.scalars().all()
    return resp_ok(data=rows)



@router.get("/ids")
async def queryids(
    db: AsyncSession = Depends(init_setup.get_async_db),
    current_user: dict = Depends(get_current_user)
):
    sql = select(DbQAgentServer)
    qb = await db.execute(sql)
    rows = qb.scalars().all()
    datas = [{"id": item.id, "name": item.name} for item in rows]
    return resp_ok(data=datas)


@router.get("/get/{id}")
async def get(
    id: int,
    db: AsyncSession = Depends(init_setup.get_async_db),
    current_user: dict = Depends(get_current_user)
):
    sql = select(DbQAgentServer).filter(DbQAgentServer.id == id)
    qb = await db.execute(sql)
    row = qb.scalar_one_or_none()
    return resp_ok(data=row)


@router.post("/add")
async def add(
    data: AddQAgent,
    db: AsyncSession = Depends(init_setup.get_async_db),
    current_user: dict = Depends(get_current_user)
):
    sql = select(DbQAgentServer).filter(DbQAgentServer.name == data.name)
    qb = await db.execute(sql)
    rows = qb.all()
    if rows and len(rows) > 0:
        return resp_fail(msg='服务名已存在')
    new_data = DbQAgentServer(**data.dict())
    db.add(new_data)
    await db.commit()
    await db.refresh(new_data)
    return resp_ok()


@router.post("/put")
async def put(
    data: PutQAgent,
    db: AsyncSession = Depends(init_setup.get_async_db),
    current_user: dict = Depends(get_current_user)
):
    if data.id is None:
        return resp_fail(msg='缺失id')
    sql = select(DbQAgentServer).filter(DbQAgentServer.id == data.id)
    qb = await db.execute(sql)
    db_obj = qb.scalar_one_or_none()
    if not db_obj:
        return resp_fail(msg='服务名不存在')
    update_data = data.dict(exclude_unset=True)
    # 循环赋值：只更新传了值的字段
    for key, value in update_data.items():
        setattr(db_obj, key, value)
    await db.commit()
    await db.refresh(db_obj)
    return resp_ok()


@router.post("/del")
async def delete(
    data: List[int],
    db: AsyncSession = Depends(init_setup.get_async_db),
    current_user: dict = Depends(get_current_user)
):
    if data is None or len(data) == 0:
        return resp_fail(msg='缺失id')
    sql = select(DbQAgentServer).filter(DbQAgentServer.id.in_(data))
    qb = await db.execute(sql)
    db_objs = qb.scalars().all()
    if not db_objs or len(db_objs) == 0:
        return resp_fail(msg='服务id不存在')
    for db_obj in db_objs:
        await db.delete(db_obj)
    await db.commit()
    return resp_ok()
