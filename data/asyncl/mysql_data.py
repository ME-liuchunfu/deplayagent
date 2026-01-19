
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from setting import DataBaseSettings
from urllib.parse import quote_plus

class InitSetup:

    def setup_mysql(self, db_config: DataBaseSettings):
        ASYNC_DATABASE_URL = f"mysql+asyncmy://{quote_plus(db_config.database_user)}:{quote_plus(db_config.database_passwd)}@{db_config.database_host}:{db_config.database_port}/{db_config.database_dbname}"
        if db_config.database_param is not None:
            ASYNC_DATABASE_URL = f'{ASYNC_DATABASE_URL}?{db_config.database_param}'
        else:
            ASYNC_DATABASE_URL = f'{ASYNC_DATABASE_URL}?charset=utf8mb4&serverTimezone=UTC'

        self.ASYNC_DATABASE_URL = ASYNC_DATABASE_URL
        # 创建异步引擎：echo=True 打印SQL语句，开发阶段建议开启，生产关闭
        self.async_engine = async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)
        # 创建异步会话工厂
        self.AsyncSessionLocal = AsyncSessionLocal = sessionmaker(
            async_engine, class_=AsyncSession, expire_on_commit=False
        )

    # ============ 6. 异步数据库会话依赖（核心，必须async/await）
    async def get_async_db(self):
        db = self.AsyncSessionLocal()
        try:
            yield db
        finally:
            await db.close()  # 异步关闭会话


init_setup = InitSetup()
