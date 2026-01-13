from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

from data.asyncl.mysql_data import init_setup
Base = declarative_base()


class MySQLORM:

    def setup(self, app):
        @app.on_event("startup")
        async def startup_event():
            """项目启动时自动执行：创建所有数据库表"""
            async_engine = init_setup.async_engine
            async with async_engine.begin() as conn:
                # 可选：删除所有表（开发阶段测试用）
                # await conn.run_sync(Base.metadata.drop_all)
                # 创建所有表
                await conn.run_sync(Base.metadata.create_all)


class DockerServer(Base):
    __tablename__ = 'docker_server'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), index=True, nullable=False)
    domain = Column(String(128), index=False, nullable=False)
    username = Column(String(128), index=False, nullable=False)
    passwd = Column(String(128), index=False, nullable=False)


class DbAuthUser(Base):
    __tablename__ = 'db_auth_user'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nickname = Column(String(128), index=False, nullable=False)
    username = Column(String(50), index=True, nullable=False)
    passwd = Column(String(128), index=False, nullable=False)
    status = Column(Integer, index=False, nullable=False)


mysql_orm = MySQLORM()
