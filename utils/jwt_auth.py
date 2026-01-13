# utils/jwt_auth.py
from datetime import datetime, timedelta
from typing import Optional, Union, Dict, Any

import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# 导入全局配置
from setting import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# ========== 密码加密校验配置 ==========
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# ========== OAuth2认证方案：指定Token的请求头格式 ==========
# 前端请求时，请求头必须传：Authorization: Bearer <你的Token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# ========== 密码加密/校验方法 ==========
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """校验明文密码和加密密码是否匹配"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """对明文密码进行bcrypt加密"""
    return pwd_context.hash(password)


# ========== JWT Token生成 ==========
def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    生成JWT Token
    :param data: 要存入Token的用户信息（建议只存id/用户名等轻量信息）
    :param expires_delta: 过期时间，不传则用全局配置
    :return: 加密后的Token字符串
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # 向Token中写入过期时间
    to_encode.update({"exp": expire})
    # 生成Token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ========== 依赖项：校验Token+解析用户信息（核心！！！） ==========
async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """
    核心依赖项：所有需要鉴权的接口，直接注入该依赖即可
    1. 校验请求头中的Token是否有效
    2. 解析Token中的用户信息
    3. Token无效/过期/篡改 → 抛出401未授权异常
    """
    # 定义异常信息，统一返回401
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="认证失败：Token无效或已过期",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 解析Token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # 从Token中获取用户ID（你可以根据业务加username/role等）
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        # 返回解析后的用户信息
        return {"user_id": int(user_id)}
    except Exception:
        # Token过期/签名错误/篡改 都会触发JWTError
        raise credentials_exception