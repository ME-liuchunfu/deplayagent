"""
服务器配置版本
"""
import os
import uuid

app_env = os.getenv('APP_ENV')
if app_env is None:
    app_env = ".env"

app_port = os.getenv('APP_PORT')
if app_port is None:
    app_port = 9000

random_token = uuid.uuid4().hex