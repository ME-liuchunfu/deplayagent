import logging

from data.jpa import jpacompement
from data.jpa.models import ServerMachine, ContainerPods
from shell.remote_shell import ssh_exec_command
from utils import json_utils


logger = logging.getLogger(__name__)

def query_server_nodes():
    """
    查询服务器节点
    :return:
    """
    servers_machine = jpacompement.JpaServerMachine.query_list()
    if len(servers_machine) > 0:
        print('当前 已有服务器如下：')
        print('序号:\t服务器ID:\t服务器名:\t')
        for i, server in enumerate(servers_machine):
            print(f'{i}\t{server.id}\t{server.name}')
        a = input('输入q退出，序号进入服务器操作,a新增服务器:')
        if not (a.count('a') > 0 or a.count('q') > 0):
            a = int(a)
            enter_server_node_machine(servers_machine[a])
        else:
            if a.count('a') > 0:
                add_server_node_machine()
    else:
        print('当前没有镜像')
        a = input('输入q退出,a新增服务器')
        if a.count('a') > 0:
            add_server_node_machine()


def add_server_node_machine():
    server_machine = ServerMachine()
    try:
        server_machine.name = input('请输入服务器名:')
        server_machine.host = input('请输入host:')
        server_machine.port = int(input('请输入port:'))
        server_machine.username = input('请输入username:')
        server_machine.password = input('请输入password:')
        server_machine.remark = input('请输入remark:')
        jpacompement.JpaServerMachine.add_machine(server_machine)
        print(f'服务器节点新增成功:{json_utils.dumps(server_machine.__dict__)}')
        a = input('输入q退出,输入n继续新增:')
        if a.count('n') > 0:
            add_server_node_machine()
    except Exception as e:
        logger.error(f'服务器节点新增错误:{json_utils.dumps(server_machine.__dict__)}', exc_info=True)
        print(f'服务器节点新增错误:{json_utils.dumps(server_machine.__dict__)}')


def add_server_container_pod(server_machine:ServerMachine):
    print(f'新增pod，server_machine：{json_utils.dumps(server_machine.__dict__)}')
    logger.info(f'新增pod，server_machine：{json_utils.dumps(server_machine.__dict__)}')
    container_pod = ContainerPods()
    container_pod.server_id = server_machine.id
    container_pod.name = input('pod名：')
    container_pod.container_id = input('容器名：')
    container_pod.command_path = input('容器路径：')
    container_pod.images_id = input('镜像id：')
    container_pod.images_name = input('镜像名：')
    container_pod.status = input('status（0停用1启用）：')
    pods_list = jpacompement.JpaContainerPods.query_list_by_machine_id(server_machine.id)
    pods_name = [p.container_id for p in pods_list]
    if container_pod.container_id in pods_name:
        print(f'当前container_id：{container_pod.container_id} 已存在')
        logger.info(f'当前container_id：{container_pod.container_id} 已存在')
        return
    jpacompement.JpaContainerPods.add_container_pods(container_pod)


def enter_server_pods_version(server_machine:ServerMachine, pods:ContainerPods):
    print(f'查看容器pod版本信息:{json_utils.dumps(pods.__dict__)}')
    logger.info(f'查看容器pod版本信息:{json_utils.dumps(pods.__dict__)}')
    container_pods_version = jpacompement.JpaContainerPodsVersion.query_pods_version_by_pods_id(pods.id)
    if len(container_pods_version) == 0:
        print('当前容器没有版本记录')
        logger.info('当前容器没有版本记录')
    else:
        print(f'查询到容器版本信息')
        logger.info(f'查询到容器版本信息, {container_pods_version}')
        print(f'序号:\t,名称:\t镜像id:\t镜像名:')
        for i, pod in enumerate(container_pods_version):
            print(f'{i}\t{pod.name}\t{pod.images_id}\t{pod.images_name}')
        n = input('q退出，r回滚')
        n = n.strip()
        if n == 'r':
            num = int(input('请输入回滚序号:'))
            pods_version = container_pods_version[num]
            ok = input(f'确认回滚吗?（y确认） :version:{json_utils.dumps(pods_version.__dict__)}')
            if ok.count('y') > 0:
                pass


def enter_server_container_pod(server_machine:ServerMachine, pods:ContainerPods):
    pull_url = None
    while True:
        print(f'进入容器节点：{json_utils.dumps(pods.__dict__)}')
        logger.info(f'进入容器节点：{json_utils.dumps(pods.__dict__)}')
        n = input('q退出，h查看历史版本,pull拉取镜像,down下架容器,up上架容器')
        n = n.strip()
        if n == 'q':
            break
        if n == 'h':
            enter_server_pods_version(server_machine, pods)
        if n == 'pull':
            pull_url = input('请输入镜像地址')
            result = ssh_exec_command(
                host=server_machine.host,
                port=server_machine.port,
                username=server_machine.username,
                password=server_machine.password,
                command=f"docker pull {pull_url}",
                timeout=60
            )
            print(f'response==> {json_utils.dumps(result.__dict__)}')
            logger.info(f'response==> {json_utils.dumps(result.__dict__)}')
        if n == 'down':
            if pull_url:
                # 先更新docker-compose
                cmd = f"sed -i 's/\(image: \).*/\1{pull_url}/' {pods.command_path}/docker-compose.yml"
                result = ssh_exec_command(
                    host=server_machine.host,
                    port=server_machine.port,
                    username=server_machine.username,
                    password=server_machine.password,
                    command=cmd,
                    timeout=10
                )
                print(f'替换docker-compose.yml镜像：response==> {json_utils.dumps(result.__dict__)}')
                logger.info(f'替换docker-compose.yml镜像：response==> {json_utils.dumps(result.__dict__)}')

            result = ssh_exec_command(
                host=server_machine.host,
                port=server_machine.port,
                username=server_machine.username,
                password=server_machine.password,
                command=f"docker compose down",
                timeout=60
            )
            print(f'response==> {json_utils.dumps(result.__dict__)}')
            logger.info(f'response==> {json_utils.dumps(result.__dict__)}')
        if n == 'up':
            result = ssh_exec_command(
                host=server_machine.host,
                port=server_machine.port,
                username=server_machine.username,
                password=server_machine.password,
                command=f"docker compose up -d",
                timeout=60
            )
            print(f'response==> {json_utils.dumps(result.__dict__)}')
            logger.info(f'response==> {json_utils.dumps(result.__dict__)}')
    print(f'退出容器pod：{json_utils.dumps(pods.__dict__)}')
    logger.info(f'退出容器pod：{json_utils.dumps(pods.__dict__)}')



def enter_server_node_pods(server_machine:ServerMachine):
    print(f'进入pods， server_machine：{json_utils.dumps(server_machine.__dict__)}')
    logger.info(f'进入pods， server_machine：{json_utils.dumps(server_machine.__dict__)}')
    container_pods = jpacompement.JpaContainerPods.query_list_by_machine_id(server_machine.id)
    if len(container_pods) > 0:
        print('当前 已有服务器pods如下：')
        print('序号:\tpod_id:\t服务器名:\t容器名称:\t状态:\t镜像id:\t镜像名:')
        for i, server in enumerate(container_pods):
            print(f'{i}\t{server.id}\t{server.name}\t{server.container_id}\t{server.status}\t{server.images_id}\t{server.images_name}')
        a = input('输入q退出，序号进入服务器操作,a新增服务pod:')
        if not (a.count('a') > 0 or a.count('q') > 0):
            a = int(a)
            enter_server_container_pod(server_machine, container_pods[a])
        else:
            if a.count('a') > 0:
                add_server_container_pod(server_machine)
    else:
        print('当前没有镜像')
        a = input('输入q退出,a新增服务器')
        if a.count('a') > 0:
            add_server_node_machine()


def enter_server_node_machine(server_machine: ServerMachine):
    try:
        a = input('输入q退出，u更改，d删除，l登录，p进入pods节点：')
        if a.count('u') > 0:
            server_machine.name = input(f"{server_machine.name} ?:")
            server_machine.host = input(f"{server_machine.host} ?:")
            server_machine.port = int(input(f"{server_machine.port} ?:"))
            server_machine.username = input(f"{server_machine.username} ?:")
            server_machine.password = input(f"{server_machine.password} ?:")
            server_machine.remark = input(f"{server_machine.remark} ?:")
            jpacompement.JpaServerMachine.update_machine(server_machine)
        if a.count('d') > 0:
            jpacompement.JpaServerMachine.del_machine(server_machine.id)
        if a.count('l') > 0:
            login_server_machine(server_machine)
        if a.count('p') > 0:
            enter_server_node_pods(server_machine)
    except Exception as e:
        logger.error(f'服务器节点错误:{server_machine.__dict__}', exc_info=True)

def login_server_machine(server_machine: ServerMachine):
    print(f'正在登录服务器节点：{server_machine.name}')
    from shell.remote_shell import ssh_interactive_connect
    ssh_interactive_connect(
        host=server_machine.host,
        username=server_machine.username,
        password=server_machine.password,
        port=server_machine.port
    )
    print(f'bye bye~~~')