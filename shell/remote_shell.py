"""
远程shell脚本
"""
import os
import paramiko
from scp import SCPClient, SCPException
from typing import Optional, List, Tuple


class SSHSCPTool:
    """Python SSH 远程连接与 SCP 文件传输工具类"""

    def __init__(
            self,
            host: str,
            port: int = 22,
            username: str = "root",
            password: Optional[str] = None,
            private_key: Optional[str] = None,
            private_key_password: Optional[str] = None
    ):
        """
        初始化 SSH 连接配置
        :param host: 远程服务器 IP 或域名
        :param port: SSH 端口（默认 22）
        :param username: 登录用户名（默认 root）
        :param password: 登录密码（与 private_key 二选一）
        :param private_key: 私钥文件路径（如 ~/.ssh/id_rsa）
        :param private_key_password: 私钥密码（若私钥加密）
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.private_key = private_key
        self.private_key_password = private_key_password

        # SSH 客户端对象
        self.ssh_client: Optional[paramiko.SSHClient] = None
        # SCP 客户端对象
        self.scp_client: Optional[SCPClient] = None

    def _connect(self) -> None:
        """建立 SSH 连接（内部调用，自动处理密钥/密码认证）"""
        if self.ssh_client and self.ssh_client.get_transport().is_active():
            return  # 已连接则直接返回

        # 初始化 SSH 客户端
        self.ssh_client = paramiko.SSHClient()
        # 自动添加远程主机密钥（避免首次连接时的手动确认）
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            # 认证方式：优先使用私钥，其次密码
            auth_kwargs = {}
            if self.private_key:
                # 加载私钥（支持加密私钥）
                private_key_obj = paramiko.RSAKey.from_private_key_file(
                    filename=self.private_key,
                    password=self.private_key_password
                )
                auth_kwargs["pkey"] = private_key_obj
            else:
                auth_kwargs["password"] = self.password

            # 建立连接
            self.ssh_client.connect(
                hostname=self.host,
                port=self.port,
                username=self.username,
                **auth_kwargs,
                timeout=10  # 连接超时时间（秒）
            )

            # 初始化 SCP 客户端
            self.scp_client = SCPClient(self.ssh_client.get_transport(), socket_timeout=30)
            print(f"✅ 成功连接到 {self.username}@{self.host}:{self.port}")

        except paramiko.AuthenticationException:
            raise Exception("❌ 认证失败：用户名/密码/私钥错误")
        except FileNotFoundError:
            raise Exception(f"❌ 私钥文件不存在：{self.private_key}")
        except Exception as e:
            raise Exception(f"❌ 连接失败：{str(e)}")

    def execute_command(self, command: str, sudo: bool = False) -> Tuple[str, str, int]:
        """
        执行远程命令
        :param command: 要执行的命令（如 "ls -l"）
        :param sudo: 是否以 sudo 权限执行（需确保用户有 sudo 权限且无需密码）
        :return: (stdout, stderr, return_code) 命令输出、错误信息、返回码
        """
        if sudo:
            command = f"sudo {command}"

        self._connect()
        try:
            stdin, stdout, stderr = self.ssh_client.exec_command(
                command,
                get_pty=True,  # 解决某些命令需要终端的问题（如 sudo）
                timeout=60  # 命令执行超时时间（秒，可根据需求调整）
            )
            # 读取输出（解码为字符串）
            stdout_str = stdout.read().decode("utf-8", errors="ignore").strip()
            stderr_str = stderr.read().decode("utf-8", errors="ignore").strip()
            return_code = stdout.channel.recv_exit_status()  # 获取返回码（0 为成功）
            return stdout_str, stderr_str, return_code
        except Exception as e:
            raise Exception(f"❌ 命令执行失败：{str(e)}")

    def upload_file(
            self,
            local_path: str,
            remote_path: str,
            recursive: bool = False,
            preserve_times: bool = True
    ) -> None:
        """
        上传本地文件/目录到远程服务器
        :param local_path: 本地文件/目录路径（绝对路径或相对路径）
        :param remote_path: 远程目标路径（目录需存在，否则报错）
        :param recursive: 是否递归上传（上传目录时必须设为 True）
        :param preserve_times: 是否保留文件原始时间戳
        """
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"❌ 本地路径不存在：{local_path}")

        self._connect()
        try:
            print(f"📤 正在上传 {local_path} -> {self.host}:{remote_path}")
            self.scp_client.put(
                local_path=local_path,
                remote_path=remote_path,
                recursive=recursive,
                preserve_times=preserve_times
            )
            print(f"✅ 上传成功")
        except SCPException as e:
            raise Exception(f"❌ 上传失败：{str(e)}")
        except Exception as e:
            raise Exception(f"❌ 上传异常：{str(e)}")

    def download_file(
            self,
            remote_path: str,
            local_path: str,
            recursive: bool = False,
            preserve_times: bool = True
    ) -> None:
        """
        从远程服务器下载文件/目录到本地
        :param remote_path: 远程文件/目录路径
        :param local_path: 本地目标路径（目录需存在，否则报错）
        :param recursive: 是否递归下载（下载目录时必须设为 True）
        :param preserve_times: 是否保留文件原始时间戳
        """
        if not os.path.isdir(local_path):
            raise NotADirectoryError(f"❌ 本地目标路径不是目录：{local_path}")

        self._connect()
        try:
            print(f"📥 正在下载 {self.host}:{remote_path} -> {local_path}")
            self.scp_client.get(
                remote_path=remote_path,
                local_path=local_path,
                recursive=recursive,
                preserve_times=preserve_times
            )
            print(f"✅ 下载成功")
        except SCPException as e:
            raise Exception(f"❌ 下载失败：{str(e)}")
        except Exception as e:
            raise Exception(f"❌ 下载异常：{str(e)}")

    def close(self) -> None:
        """关闭 SSH 和 SCP 连接"""
        try:
            if self.scp_client:
                self.scp_client.close()
            if self.ssh_client:
                self.ssh_client.close()
            print(f"🔌 已断开与 {self.host} 的连接")
        except Exception as e:
            print(f"⚠️  关闭连接时警告：{str(e)}")

    def __enter__(self):
        """支持 with 语句自动连接"""
        self._connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """支持 with 语句自动关闭连接"""
        self.close()

