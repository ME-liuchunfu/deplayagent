import json
import logging
from pickle import FALSE
from xmlrpc.client import Fault

from data.jpa import jpacompement
from data.jpa.models import NginxBlsMachine, ServerMachine, NginxBlsWeight
from shell.remote_shell import ssh_exec_command


logger = logging.getLogger(__name__)

def query_nginx_bls():
    """
    查询nginx负载
    :return:
    """
    nginx_bls_machines = jpacompement.JpaNginxBlsMachine.query_list()
    if len(nginx_bls_machines) > 0:
        print('当前 已有nginx bls如下：')
        print('序号:\tbls名称:\t服务器id:\t是否容器:\t配置路径:')
        for i, server in enumerate(nginx_bls_machines):
            print(f'{i}\t{server.name}\t{server.server_id}\t{server.container_machine}\t{server.command_config_path}')
        a = input('输入q退出，序号进入服务器操作,a新增服务器:')
        if not (a.count('q')>0 or a.count('a')>0):
            a = int(a)
            enter_nginx_bls_machine(nginx_bls_machines[a])
        else:
            if a.count('a') > 0:
                add_nginx_bls_machine()
    else:
        print(f'当前没有nginx负载信息')
        a = input('输入q退出，a新增:')
        if a.count('a') > 0:
            add_nginx_bls_machine()


def add_nginx_bls_machine():
    nginx_bls_machine = NginxBlsMachine()
    try:
        nginx_bls_machine.name = input('nginx bls名称:')
        nginx_bls_machine.server_id = int(input('主机服务id:'))
        tf = input('是否容器（0否1是）:')
        nginx_bls_machine.container_machine = True if tf.count('1') else False
        nginx_bls_machine.container_id = input('容器id:')
        nginx_bls_machine.command_path = input('程序路径（容器不用填）:')
        nginx_bls_machine.command_config_path = input('配置路径:')
        nginx_bls_machine.status = input('状态（0停用,1启用）:')
        jpacompement.JpaNginxBlsMachine.add_nginx_bls_machine(nginx_bls_machine)
    except Exception as e:
        logger.error(f'新增nginx负载错误:{nginx_bls_machine.__dict__}', exc_info=True)


def add_nginx_bls_weight(server_node: ServerMachine, nginx_bls_machine: NginxBlsMachine):
    print(f'增加bls node weight节点配置：{json.dumps(nginx_bls_machine.__dict__, indent=2, ensure_ascii=False)}')
    nginx_bls_weight = NginxBlsWeight()
    nginx_bls_weight.bls_machine_id = nginx_bls_machine.id
    nginx_bls_weight.name = input('bls weight名称：')
    nginx_bls_weight.command_config_path = input('command_config_path路径：')
    nginx_bls_weight.status = input('status(0停用1启用)：')
    jpacompement.JpaNginxBlsWeight.add_nginx_bls_weight(nginx_bls_weight)
    print(f'新增完成{json.dumps(nginx_bls_weight.__dict__, indent=2, ensure_ascii=False)}')


def enter_nginx_bls_weight(server_node: ServerMachine, nginx_bls_machine: NginxBlsMachine):
    print(f'进入server {server_node.name} node: {nginx_bls_machine.name}')
    bls_weight_nodes = jpacompement.JpaNginxBlsWeight.query_list_by_bls_machine_id(nginx_bls_machine.id)
    if len(bls_weight_nodes) > 0:
        print('当前 已有nginx bls weight如下：')
        print('序号:\tbls weight名称:\tconfig_path:\tstatus:')
        for i, weight in enumerate(bls_weight_nodes):
            print(f"{i}\t{weight.name}\t{weight.command_config_path}\t{weight.status}")
        a = input('q退出,序号进入节点，a新增节点')
        if a.count('a') > 0:
            add_nginx_bls_weight(server_node, nginx_bls_machine)
        else:
            if a.count('q') == 0:
                a = int(a)
                node = bls_weight_nodes[a]
                print(f'当前选择节点:{node.name}')
                n = input('q退出，d删除，up使用当前节点，oup仅使用当前节点')
                n = n.strip()
                if n == 'd':
                    jpacompement.JpaNginxBlsWeight.del_nginx_bls_weight(node.id)
                    print(f'已删除 bls weight:{node.id}')
                if n == 'up':
                    node.command_config_path = node.command_config_path.replace('_bak', '')
                    command = f'mv {node.command_config_path}_bak {node.command_config_path}'
                    result = ssh_exec_command(
                        host=server_node.host,
                        port=server_node.port,
                        username=server_node.username,
                        password=server_node.password,
                        command=command,
                        timeout=30
                    )
                    print(f"节点配置更新：{result.__dict__}")
                    logger.info(f"节点配置更新：{result.__dict__}")
                    jpacompement.JpaNginxBlsWeight.update_nginx_bls_weight(node)
                    result = ssh_exec_command(
                        host=server_node.host,
                        port=server_node.port,
                        username=server_node.username,
                        password=server_node.password,
                        command=f"docker exec -i {nginx_bls_machine.container_id} nginx -t",
                        timeout=30
                    )
                    print(f'bls node weight 检测结果：{result.__dict__}')
                    logger.info(f'bls node weight 检测结果：{result.__dict__}')
                    if result.success and result.stdout.count('test is successful') > 0:
                        # 执行更新
                        while True:
                            result1 = ssh_exec_command(
                                host=server_node.host,
                                port=server_node.port,
                                username=server_node.username,
                                password=server_node.password,
                                command=f"docker exec -i {nginx_bls_machine.container_id} nginx -s reload",
                                timeout=30
                            )
                            print(f'bls node weight 结果：{result1.__dict__}')
                            logger.info(f'bls node weight 结果：{result1.__dict__}')
                            at = input('q退出')
                if n == 'oup':
                    bak_que = {p.id: f"mv {p.command_config_path} {p.command_config_path}_bak" for p in bls_weight_nodes if not p.command_config_path.endswith('_bak') and p.command_config_path != node.command_config_path}
                    reload_flag = False
                    if node.command_config_path.endswith('_bak'):
                        reload_flag = True
                        command = f'mv {node.command_config_path} {node.command_config_path.replace("_bak", "")}'
                        result = ssh_exec_command(
                            host=server_node.host,
                            port=server_node.port,
                            username=server_node.username,
                            password=server_node.password,
                            command=command,
                            timeout=30
                        )
                        print(f"节点配置更新：{result.__dict__}")
                        logger.info(f"节点配置更新：{result.__dict__}")
                        if result.success:
                            node.command_config_path = node.command_config_path.replace("_bak", '')
                            node.status = 1
                        else:
                            node.status = 0
                        jpacompement.JpaNginxBlsWeight.update_nginx_bls_weight(node)
                    if len(bak_que) > 0:
                        reload_flag = True
                        for k in bak_que:
                            q = bak_que.get(k)
                            result = ssh_exec_command(
                                host=server_node.host,
                                port=server_node.port,
                                username=server_node.username,
                                password=server_node.password,
                                command=q,
                                timeout=30
                            )
                            print(f'备份节点结果：{result.__dict__}')
                            logger.info(f'备份节点结果：{result.__dict__}')
                            for p in bls_weight_nodes:
                                if p.id == k and result.success:
                                    p.command_config_path = p.command_config_path.replace('_bak', '')
                                    p.command_config_path = f"{p.command_config_path}_bak"
                                    p.status = 0
                                    jpacompement.JpaNginxBlsWeight.update_nginx_bls_weight(p)
                    if reload_flag:
                        result = ssh_exec_command(
                            host=server_node.host,
                            port=server_node.port,
                            username=server_node.username,
                            password=server_node.password,
                            command=f"docker exec -i {nginx_bls_machine.container_id} nginx -t",
                            timeout=30
                        )
                        print(f'bls node weight 检测结果：{result.__dict__}')
                        logger.info(f'bls node weight 检测结果：{result.__dict__}')
                        if result.success and result.stdout.count('test is successful') > 0:
                            # 执行更新
                            while True:
                                result1 = ssh_exec_command(
                                    host=server_node.host,
                                    port=server_node.port,
                                    username=server_node.username,
                                    password=server_node.password,
                                    command=f"docker exec -i {nginx_bls_machine.container_id} nginx -s reload",
                                    timeout=30
                                )
                                print(f'bls node weight 结果：{result1.__dict__}')
                                logger.info(f'bls node weight 结果：{result1.__dict__}')
                                at = input('q退出，其他继续重载')
                                if at.count('q') > 0:
                                    break
    else:
        a = input('q退出，a新增节点')
        if a.count('a') > 0:
            add_nginx_bls_weight(server_node, nginx_bls_machine)


def enter_nginx_bls_machine(nginx_bls_machine: NginxBlsMachine):
    server_node = jpacompement.JpaServerMachine.query_by_id(nginx_bls_machine.server_id)
    if server_node is None:
        print(f'找不到server node：{nginx_bls_machine.server_id}')
        return
    while True:
        print(f'nginx_bls_machine:{json.dumps(nginx_bls_machine.__dict__,indent=2, ensure_ascii=False)}')
        a = input('q退出,w进入负载项，执行命令请输入:')
        if a.strip() == 'q':
            break
        if a.strip() == 'w':
            enter_nginx_bls_weight(server_node, nginx_bls_machine)
            continue
        command = a
        result = ssh_exec_command(
            host=server_node.host,
            port=server_node.port,
            username=server_node.username,
            password=server_node.password,
            command=command,
            timeout=30
        )
        logger.info(f"response ==> {result.__dict__}")
        # print(result.__dict__)
        if result.success:
            print(f"response ==> \n{result.stdout}")
        else:
            print(f"response error ==> \n{result.stderr}")

