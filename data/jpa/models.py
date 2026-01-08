"""
数据库表操作层
"""
from dataclasses import dataclass, field


@dataclass
class ServerMachine:
    """
    服务器主机资源
    """

    id: int = field(default_factory=lambda :-1)
    name: str = field(default_factory=lambda : None)
    host: str = field(default_factory=lambda : None)
    port: int = field(default_factory=lambda : 22)
    username: str = field(default_factory=lambda : None)
    password: str = field(default_factory=lambda : None)
    private_key: str = field(default_factory=lambda : None)
    private_key_password: str = field(default_factory=lambda : None)
    remark: str = field(default_factory=lambda : None)


@dataclass
class NginxBlsMachine:
    """
    nginx 负载主机
    """

    id: int = field(default_factory=lambda: -1)
    name: str = field(default_factory=lambda: None)
    # ServerMachine 外键
    server_id: int = field(default_factory=lambda : -1)
    # 是否是容器
    container_machine: bool = field(default_factory=lambda : False)
    container_id: str = field(default_factory=lambda : None)
    command_path: str = field(default_factory=lambda : None)
    command_config_path: str = field(default_factory=lambda : None)
    status: str = field(default_factory=lambda : None)


@dataclass
class ContainerPods:
    """
    服务容器主机
    """
    id: int = field(default_factory=lambda: -1)
    name: str = field(default_factory=lambda: None)
    # ServerMachine 外键
    server_id: int = field(default_factory=lambda: -1)
    container_id: str = field(default_factory=lambda: None)
    command_path: str = field(default_factory=lambda: None)
    images_id: str = field(default_factory=lambda : None)
    images_name: str = field(default_factory=lambda : None)
    status: str = field(default_factory=lambda : None)


@dataclass
class ImagesInfos:
    """
    镜像信息
    """
    id: int = field(default_factory=lambda: -1)
    images_id: str = field(default_factory=lambda: None)
    images_name: str = field(default_factory=lambda: None)
    images_version: str = field(default_factory=lambda: None)
    images_size: str = field(default_factory=lambda : None)
