"""
数据库操作基础层
"""

import logging
from typing import Optional, Union, List
from pymysql import OperationalError, connect as mysql_connect, \
    cursors, Connection
from pymysql.cursors import Cursor
from setting import DataBaseSettings

logger = logging.getLogger(__name__)


def connect_to_mysql(dbConfig: DataBaseSettings) -> Optional[Connection]:
    # 建立连接
    connection = mysql_connect(
        host=dbConfig.database_host,
        database=dbConfig.database_dbname,
        user=dbConfig.database_user,
        password=dbConfig.database_passwd,
        charset=dbConfig.database_charset,
        cursorclass=cursors.DictCursor  # 使查询结果以字典形式返回
    )
    connection.cursor()
    logger.info("成功连接到MySQL数据库")
    return connection


def close_connect(connection: Optional[Connection] = None):
    if connection is not None:
        connection.close()
        logger.info("MySQL连接已关闭")


def close_cursor(cursor=None):
    if cursor is not None:
        cursor.close()
        logger.info("cursor连接已关闭")


def close(closeable: Union[Connection, Cursor, List] = None):
    if closeable is None:
        return
    if isinstance(closeable, Connection):
        close_connect(closeable)
    if isinstance(closeable, Cursor):
        close_cursor(closeable)
    if isinstance(closeable, List):
        for able in closeable:
            if able is None:
                continue
            if isinstance(able, Connection):
                close_connect(able)
            if isinstance(able, Cursor):
                close_cursor(able)