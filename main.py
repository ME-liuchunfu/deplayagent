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

from application_config import app_port
from data.asyncl.mysql_data import init_setup
from data.asyncl.mysql_orm import Base
from setting import settings
from logconfig import setup_rotating_log
from task.qagent_container_task import sync_qagent_container
from web import resp_fail
from web.api import (hub_docker_api, hub_docker_registry_api,
                     auth_api, qagent_server_api, qagent_server_client_api,
                    qagent_server_container_api
                     )
from data.asyncl import mysql_data, mysql_orm
from task import schedule_task


log_dir = "./logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir, exist_ok=True)

setup_rotating_log(log_file=f"{log_dir}/app.log")
logger = logging.getLogger(__name__)


async def lifespan(app: FastAPI):
    async_engine = init_setup.async_engine
    async with async_engine.begin() as conn:
        # 可选：删除所有表（开发阶段测试用）
        # await conn.run_sync(Base.metadata.drop_all)
        # 创建所有表
        await conn.run_sync(Base.metadata.create_all)
    schedule_task.start()
    sync_qagent_container()
    yield
    logger.info("✅ FastAPI服务关闭，后台定时任务线程已停止")


app = FastAPI(
        title="deplayagent",
        description="",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有前端域名访问，生产环境建议指定具体域名，如["http://localhost:3000"]
    allow_credentials=True,  # 允许携带Cookie
    allow_methods=["*"],  # 允许所有请求方法：GET/POST/PUT/DELETE等
    allow_headers=["*"],  # 允许所有请求头
)

mysql_data.init_setup.setup_mysql(db_config=settings.database)


# 路由
app.include_router(hub_docker_api.router, prefix='/api/hub/docker/machine', tags=['hub-docker-machine'])
app.include_router(hub_docker_registry_api.router, prefix='/api/hub/docker/registry', tags=['hub-docker-registry'])
app.include_router(auth_api.router, prefix="/api/auth", tags=['auth'])
app.include_router(qagent_server_api.router, prefix="/api/qagent/server", tags=['QAgentServer'])
app.include_router(qagent_server_client_api.router, prefix="/api/qagent/server_client", tags=['QAgentServer client'])
app.include_router(qagent_server_container_api.router, prefix="/api/qagent/server_container", tags=['QAgentServer container'])


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
    uvicorn.run("main:app", host="0.0.0.0", port=app_port, reload=False)
