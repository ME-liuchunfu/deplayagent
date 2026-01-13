"""
gui程序入口
"""
import logging
import os.path
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from setting import settings
from logconfig import setup_rotating_log
from web import resp_fail
from web.api import hub_docker_api, hub_docker_registry_api, auth_api
from data.asyncl import mysql_data, mysql_orm


log_dir = "../deplayagent-logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir, exist_ok=True)

setup_rotating_log(log_file="../deplayagent-logs/app.log")
logger = logging.getLogger(__name__)

app = FastAPI(
        title="deplayagent",
        description="",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有前端域名访问，生产环境建议指定具体域名，如["http://localhost:3000"]
    allow_credentials=True,  # 允许携带Cookie
    allow_methods=["*"],  # 允许所有请求方法：GET/POST/PUT/DELETE等
    allow_headers=["*"],  # 允许所有请求头
)

mysql_data.init_setup.setup_mysql(db_config=settings.database)
mysql_orm.mysql_orm.setup(app)


# 路由
app.include_router(hub_docker_api.router, prefix='/api/hub/docker/machine', tags=['hub-docker-machine'])
app.include_router(hub_docker_registry_api.router, prefix='/api/hub/docker/registry', tags=['hub-docker-registry'])
app.include_router(auth_api.router, tags=['auth'])


# ============ 2. 集成全局异常捕获 ============
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """捕获：参数校验失败异常（Pydantic校验失败）"""
    logger.error(f'path:{request.url}, error:{exc}', exc_info=True)
    return JSONResponse(status_code=400, content=resp_fail(msg=f"参数错误：{exc.errors()[0]['msg']}"))

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """捕获：手动抛出的HTTP异常"""
    logger.error(f'path:{request.url}, error:{exc}', exc_info=True)
    return JSONResponse(status_code=exc.status_code, content=resp_fail(msg=exc.detail, code=exc.status_code))

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """捕获：所有未处理的全局异常（兜底）"""
    logger.error(f'path:{request.url}, error:{exc}', exc_info=True)
    return JSONResponse(status_code=500, content=resp_fail(msg=f"服务器内部错误：{str(exc)}", code=500))


if __name__ == '__main__':
    import uvicorn
    # uvicorn.run("文件名称:app实例", 主机, 端口, 是否热重载)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
