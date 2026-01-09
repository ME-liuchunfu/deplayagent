"""
远程shell脚本
"""
import os
import paramiko
import pexpect
from scp import SCPClient, SCPException
from typing import Optional, List, Tuple
import sys

from shell import ShellResult


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


def ssh_interactive_connect(host: str, port: int, username: str, password: str):
    """
    Python 实现 全交互式 SSH 远程连接
    :param host: 远程服务器IP/域名
    :param port: SSH端口，默认22
    :param username: 远程登录用户名
    :param password: 远程登录密码
    """
    # 创建SSH客户端实例
    ssh = paramiko.SSHClient()
    # 自动接受远程主机的密钥（首次连接不报错）
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # 建立SSH连接
        ssh.connect(
            hostname=host,
            port=port,
            username=username,
            password=password,
            timeout=15,
            look_for_keys=False,
            allow_agent=False,
            banner_timeout=30
        )
        print(f"✅ 成功连接远程服务器：{username}@{host}:{port}")
        print("💡 使用提示：输入任意Linux命令即可执行，输入 exit 回车 断开连接\n")

        # ========== 核心：Paramiko原生交互式Shell（Windows核心关键） ==========
        # invoke_shell() 是Paramiko内置的交互式shell，模拟真实终端，无需pty！
        channel = ssh.invoke_shell(term='xterm', width=120, height=35)
        channel.settimeout(0.01)  # 极低超时，避免阻塞，Windows友好

        # 接收并打印连接后的欢迎信息/命令提示符
        while channel.recv_ready():
            output = channel.recv(4096).decode('utf-8', errors='ignore')
            sys.stdout.write(output)
            sys.stdout.flush()

        # ========== 双向实时交互核心逻辑 ==========
        while True:
            if channel.recv_ready():
                output = channel.recv(4096).decode('utf-8', errors='ignore')
                sys.stdout.write(output)
                sys.stdout.flush()
                if not output: break

            try:
                cmd = sys.stdin.readline()
                if cmd.strip().lower() == 'exit':
                    print(f"用户主动退出，断开SSH连接")
                    channel.send(cmd)
                    break
                channel.send(cmd)
                print(f"发送命令到服务器: {cmd.strip()}")
            except KeyboardInterrupt:
                print("用户手动中断输入")
                continue

    except paramiko.AuthenticationException:
        print("❌ 认证失败：用户名或密码错误！")
    except paramiko.SSHException as e:
        print(f"❌ SSH连接异常：{str(e)}，可能是服务器SSH服务未启动")
    except Exception as e:
        print(f"❌ 未知异常：{str(e)}")
    finally:
        # 确保连接正常关闭
        if ssh.get_transport() and ssh.get_transport().is_active():
            ssh.close()
        print("✅ SSH连接已正常断开")


def ssh_pexpect_interactive_single(host: str, user: str, password: str, port: int = 22):
    """
    pexpect 实现极简交互式SSH
    :param host: 远程IP/域名
    :param user: 用户名
    :param password: 密码
    :param port: SSH端口
    """
    # 核心命令：生成ssh连接指令
    ssh_cmd = f"ssh {user}@{host} -p {port}"
    # 启动交互式SSH进程
    child = pexpect.spawn(ssh_cmd)

    # 匹配登录过程的交互提示
    try:
        # 匹配 "password:" 密码输入提示
        child.expect("password:")
        # 输入密码并回车
        child.sendline(password)
        # 匹配远程服务器的命令行提示符（说明登录成功）
        child.expect(r"[$#>]")
        print(f"✅ 成功登录 {user}@{host}")
        print("💡 提示：输入命令交互，输入 exit 退出\n")

        # 进入完全交互模式：本地输入直接发送，远程输出直接打印
        child.interact()

    except pexpect.TIMEOUT:
        print("❌ 连接超时！")
    except pexpect.EOF:
        print("❌ 连接断开或认证失败！")
    finally:
        child.close()


def ssh_exec_command(
        host: str,
        port: int = 22,
        username: str = "",
        password: str = "",
        command: str = "",
        timeout: int = 15
) -> ShellResult:
    """
    Python 跨平台非交互式SSH执行远程命令【Windows/Linux/Mac全兼容】
    :param host: 远程服务器IP/域名
    :param port: SSH端口
    :param username: 登录用户名
    :param password: 登录密码
    :param command: 要执行的远程命令(非交互式)
    :param timeout: 连接超时时间
    :return: dict 格式化结果: {'success':布尔, 'stdout':标准输出, 'stderr':错误输出, 'msg':描述信息}
    """
    # 初始化返回结果
    result = {
        "success": False,
        "stdout": "",
        "stderr": "",
        "msg": ""
    }
    ssh_client = paramiko.SSHClient()
    # 自动接受远程主机密钥，避免首次连接报错
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # 建立SSH连接，跨平台通用配置
        ssh_client.connect(
            hostname=host,
            port=port,
            username=username,
            password=password,
            timeout=timeout,
            look_for_keys=False,  # 关闭密钥登录，纯密码登录，Windows无坑
            allow_agent=False,  # 关闭SSH代理，Windows/Linux通用
            banner_timeout=timeout * 2
        )

        # ========== 核心：非交互式执行命令 核心方法 ==========
        # exec_command 是paramiko非交互SSH的官方标准方法，无任何兼容问题
        stdin, stdout, stderr = ssh_client.exec_command(command)
        # 等待命令执行完成，获取返回码
        exit_code = stdout.channel.recv_exit_status()

        # 读取标准输出和错误输出，统一解码+处理中文乱码
        stdout_content = stdout.read().decode("utf-8", errors="ignore").strip()
        stderr_content = stderr.read().decode("utf-8", errors="ignore").strip()

        # 封装执行结果
        if exit_code == 0:
            result["success"] = True
            result["stdout"] = stdout_content
            result["msg"] = f"命令执行成功: {command}"
        else:
            result["stderr"] = stderr_content
            result["msg"] = f"命令执行失败(返回码:{exit_code}): {command}"

    except paramiko.AuthenticationException:
        result["msg"] = f"❌ 认证失败：用户名或密码错误"
    except paramiko.SSHException as e:
        result["msg"] = f"❌ SSH协议异常：{str(e)} (服务器SSH服务未启动/连接被断开)"
    except Exception as e:
        result["msg"] = f"❌ 执行异常：{str(e)}"
    finally:
        # 安全关闭连接，无论成败都执行
        try:
            if ssh_client.get_transport() and ssh_client.get_transport().is_active():
                ssh_client.close()
        except:
            pass
    return ShellResult(**result)
