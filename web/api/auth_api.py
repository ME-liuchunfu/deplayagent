# api/auth.py
import time

from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from data.asyncl.mysql_data import init_setup
from data.asyncl.mysql_orm import DbAuthUser
from utils.jwt_auth import verify_password, create_access_token
from setting import ACCESS_TOKEN_EXPIRE_MINUTES
from web import resp_ok

router = APIRouter(tags=["用户认证"])


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_minutes: int = 120
    now: int


class UserLogin(BaseModel):
    username: str
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
    access_token = create_access_token(data={"sub": str(db_user.id), 'nickname': user.username})
    # 4. 返回Token信息
    return resp_ok(data=Token(
        access_token=access_token,
        token_type="bearer",
        expires_minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
        now=int(time.time() * 1000),
    ))

