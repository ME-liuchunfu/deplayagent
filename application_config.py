"""
服务器配置版本
"""
import os

app_env = os.getenv('APP_ENV')
if app_env is None:
    app_env = ".env"
