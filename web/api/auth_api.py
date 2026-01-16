# api/auth.py
import time

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from data.asyncl.mysql_data import init_setup
from data.asyncl.mysql_orm import DbAuthUser
from utils.jwt_auth import verify_password, create_access_token, get_current_user
from setting import ACCESS_TOKEN_EXPIRE_MINUTES
from web import resp_ok
from pydantic import BaseModel, Field


router = APIRouter(tags=["用户认证"])


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_minutes: int = 120
    now: int


class UserLogin(BaseModel):
    username: str = Field(..., alias="userName", description="用户名")
    password: str


@router.post("/login", summary="用户登录，获取JWT Token")
async def login(
    user: UserLogin = Body(...),
    db: AsyncSession = Depends(init_setup.get_async_db)
):
    # 1. 根据用户名查询用户
    result = await db.execute(select(DbAuthUser).filter(DbAuthUser.username == user.username))
    db_user = result.scalar_one_or_none()
    # 2. 校验用户是否存在 + 密码是否正确
    if not db_user or not verify_password(user.password, db_user.passwd):
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    if db_user.status != 1:
        raise HTTPException(status_code=400, detail="非法账号")
    # 3. 生成Token：只存入用户ID，轻量高效
    access_token = create_access_token(data={"sub": str(db_user.id), 'nickname': db_user.nickname})
    # 4. 返回Token信息
    return resp_ok(data=Token(
        access_token=access_token,
        token_type="bearer",
        expires_minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
        now=int(time.time() * 1000),
    ))


@router.post("/reflush", summary="刷新JWT Token")
async def reflush(
    db: AsyncSession = Depends(init_setup.get_async_db),
    current_user: dict = Depends(get_current_user)
):
    # 1. 根据用户名查询用户
    user_id = current_user.get('user_id')
    result = await db.execute(select(DbAuthUser).filter(DbAuthUser.id == user_id))
    db_user = result.scalar_one_or_none()
    if db_user is None or db_user.status != 1:
        raise HTTPException(status_code=401, detail="非法账号")
    # 3. 生成Token：只存入用户ID，轻量高效
    access_token = create_access_token(data={"sub": str(db_user.id), 'nickname': db_user.nickname})
    # 4. 返回Token信息
    return resp_ok(data=Token(
        access_token=access_token,
        token_type="bearer",
        expires_minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
        now=int(time.time() * 1000),
    ))



@router.post("/info", summary="info")
async def info(
    db: AsyncSession = Depends(init_setup.get_async_db),
    current_user: dict = Depends(get_current_user)
):
    # 1. 根据用户名查询用户
    user_id = current_user.get('user_id')
    result = await db.execute(select(DbAuthUser).filter(DbAuthUser.id == user_id))
    db_user = result.scalar_one_or_none()
    if db_user is None or db_user.status != 1:
        raise HTTPException(status_code=401, detail="非法账号")
    return resp_ok(data={'name': db_user.nickname, 'avatar': '', 'username': db_user.username})
