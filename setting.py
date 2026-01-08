
from typing import Optional
from dataclasses import dataclass, field
from dotenv import load_dotenv, dotenv_values
from application_config import app_env as env_name

dotenv_dict = dotenv_values(env_name)

@dataclass
class DataBaseSettings:
    database_host: Optional[str] = field(default_factory=lambda: None)
    database_user: Optional[str] = field(default_factory=lambda: None)
    database_passwd: Optional[str] = field(default_factory=lambda: None)
    database_dbname: Optional[str] = field(default_factory=lambda: None)
    database_charset: Optional[str] = field(default_factory=lambda: None)

@dataclass
class HubRegistrySetting:
    hub_registry_url: Optional[str] = field(default_factory=lambda: None)
    hub_username: Optional[str] = field(default_factory=lambda: None)
    hub_password: Optional[str] = field(default_factory=lambda: None)


def parse_value(env_dict, clazz, lower_key: bool = True):
    try:
        db_field_names = clazz.__dataclass_fields__.keys()
        if lower_key:
            valid_kwargs = {key.lower(): value for key, value in env_dict.items() if key.lower() in db_field_names}
        else:
            valid_kwargs = {key: value for key, value in env_dict.items() if key in db_field_names}
        return clazz(**valid_kwargs)
    except Exception as e:
        print(e)

class Settings:
    """全局配置聚合"""
    database: DataBaseSettings
    hub_registry: HubRegistrySetting
    local_flag: bool

    def __init__(self):
        self.database = parse_value(dotenv_dict, DataBaseSettings, True)
        self.hub_registry = parse_value(dotenv_dict, HubRegistrySetting, True)
        self.local_flag = True


# 初始化全局配置
settings = Settings()
