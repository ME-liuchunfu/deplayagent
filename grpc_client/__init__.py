import logging
from dataclasses import dataclass, field
import grpc


logger = logging.getLogger(__name__)


@dataclass
class GrpcQAgentConfig:
    host: str = field(default="localhost")
    port: int = field(default=6305)


class GrpcQAgentClient:

    def __init__(self, conf: GrpcQAgentConfig):
        self.conf = conf
        self.channel = None
        self.connected = False

    def _get_channel(self):
        channel = grpc.insecure_channel(f'{self.conf.host}:{self.conf.port}')
        return channel

    def close(self):
        try:
            if self.channel is not None and self.connected:
                self.channel.close()
                self.channel = None
            self.connected = False
        except Exception as e:
            logger.error(f'关闭grpc QAgentClient 连接异常', exc_info=True)

    def __enter__(self):
        """进入with代码块：自动建立连接"""
        self.channel = self._get_channel()
        self.connected = True
        logger.info(f"✅ gRPC QAgent客户端已连接至: {self.conf}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出with代码块：自动释放所有资源，必执行"""
        if self.connected and self.channel:
            self.close()
            logger.info(f"✅ gRPC客户端已断开连接: {self.conf}")
        return False

