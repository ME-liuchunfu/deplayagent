from typing import Optional, List
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from data.asyncl.mysql_data import init_setup
from data.asyncl.mysql_orm import DockerServer
from web import resp_ok, resp_fail
from sqlalchemy import select


router = APIRouter()


class ListQuery(BaseModel):
    name: Optional[str] = None
    domain: Optional[str] = None


class AddDockerServer(BaseModel):
    name: str = None
    domain: str = None
    username: Optional[str] = None
    passwd: Optional[str] = None

class PutDockerServer(BaseModel):
    id: int
    name: str = None
    domain: str = None
    username: Optional[str] = None
    passwd: Optional[str] = None


@router.get("/list")
async def list(query: ListQuery = Depends(), db: AsyncSession = Depends(init_setup.get_async_db)):
    sql = select(DockerServer)
    if query.name:
         sql.filter(DockerServer.name.like(f'{query.name}%'))
    if query.domain:
         sql.filter(DockerServer.domain.like(f'{query.domain}%'))
    qb = await db.execute(sql)
    rows = qb.scalars().all()
    return resp_ok(data=rows)


@router.get("/get/{id}")
async def get(id: int, db: AsyncSession = Depends(init_setup.get_async_db)):
    sql = select(DockerServer).filter(DockerServer.id == id)
    qb = await db.execute(sql)
    row = qb.scalar_one_or_none()
    return resp_ok(data=row)


@router.post("/add")
async def add(data: AddDockerServer, db: AsyncSession = Depends(init_setup.get_async_db)):
    sql = select(DockerServer).filter(DockerServer.name == data.name)
    qb = await db.execute(sql)
    rows = qb.all()
    if rows and len(rows) > 0:
        return resp_fail(msg='服务名已存在')
    new_data = DockerServer(**data.dict())
    db.add(new_data)
    await db.commit()
    await db.refresh(new_data)
    return resp_ok()


@router.post("/put")
async def put(data: PutDockerServer, db: AsyncSession = Depends(init_setup.get_async_db)):
    if data.id is None:
        return resp_fail(msg='缺失id')
    sql = select(DockerServer).filter(DockerServer.id == data.id)
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
async def delete(data: List[int], db: AsyncSession = Depends(init_setup.get_async_db)):
    if data is None or len(data) == 0:
        return resp_fail(msg='缺失id')
    sql = select(DockerServer).filter(DockerServer.id.in_(data))
    qb = await db.execute(sql)
    db_objs = qb.scalars().all()
    if not db_objs or len(db_objs) == 0:
        return resp_fail(msg='服务id不存在')
    for db_obj in db_objs:
        await db.delete(db_obj)
    await db.commit()
    return resp_ok()
