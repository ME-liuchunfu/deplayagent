from shell.remote_shell import SSHSCPTool

# ------------------------------
# 示例：如何使用工具类
# ------------------------------
if __name__ == "__main__":
    # 1. 配置远程服务器信息（二选一：密码认证 / 私钥认证）
    # 方式1：密码认证
    ssh_config = {
        "host": "192.100.29.131",  # 远程服务器 IP
        "port": 22,
        "username": "root",
        "password": "root"  # 服务器密码
    }

    # 方式2：私钥认证（推荐，更安全）
    # ssh_config = {
    #     "host": "192.168.1.100",
    #     "port": 22,
    #     "username": "root",
    #     "private_key": "~/.ssh/id_rsa",  # 本地私钥路径
    #     "private_key_password": "your_key_password"  # 若私钥未加密，可省略
    # }

    # 2. 使用 with 语句（自动连接/关闭，推荐）
    with SSHSCPTool(**ssh_config) as ssh_scp:
        # ------------------------------
        # 示例1：执行远程命令
        # ------------------------------
        print("\n=== 执行远程命令 ===")
        # 简单命令（查看服务器信息）
        stdout, stderr, return_code = ssh_scp.execute_command("uname -a")
        print(f"命令输出：\n{stdout}")
        print(f"错误信息：{stderr}")
        print(f"返回码：{return_code}")

        # sudo 命令（需确保用户无需输入密码）
        stdout, stderr, return_code = ssh_scp.execute_command("docker --version")
        print(f"\nsudo 命令输出：\n{stdout}")

        # ------------------------------
        # 示例2：上传文件/目录
        # ------------------------------
        NEXT = False
        if NEXT:
            print("\n=== 上传文件 ===")
            # 上传单个文件
            ssh_scp.upload_file(
                local_path="./local_file.txt",  # 本地文件路径
                remote_path="/root/remote_file.txt"  # 远程目标路径（文件或目录）
            )

            # 上传目录（recursive=True）
            ssh_scp.upload_file(
                local_path="./local_dir",  # 本地目录
                remote_path="/root/remote_dir",  # 远程目录（需已存在）
                recursive=True
            )

            # ------------------------------
            # 示例3：下载文件/目录
            # ------------------------------
            print("\n=== 下载文件 ===")
            # 下载单个文件
            ssh_scp.download_file(
                remote_path="/root/remote_file.txt",  # 远程文件路径
                local_path="./downloads/"  # 本地目录（需已存在）
            )

            # 下载目录（recursive=True）
            ssh_scp.download_file(
                remote_path="/root/remote_dir",  # 远程目录
                local_path="./downloads/",  # 本地目录（需已存在）
                recursive=True
            )

    # 3. 不使用 with 语句（需手动关闭）
    # ssh_scp = SSHSCPTool(**ssh_config)
    # try:
    #     ssh_scp.execute_command("ls -l /root")
    # finally:
    #     ssh_scp.close()