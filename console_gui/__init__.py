"""
控制台程序入口
"""
import logging
from console_gui import images
from console_gui import nginx_bls
from console_gui import server_node


logger = logging.getLogger(__name__)

menus = [
    "查看 已拉取镜像",
    "查询 新版本镜像",
    "更新 新版本镜像",
    "进入nginx负载",
    "进入服务器",
]

def pl(s):
    print(s)

def print_gui_menu():
    pl("序号:\t操作:")
    for m in range(len(menus)):
        pl(f"{m}\t{menus[m]}")

menus_handles = {
    0: images.load_db_images,
    1: images.query_docker_images,
    2: images.sync_docker_images,
    3: nginx_bls.query_nginx_bls,
    4: server_node.query_server_nodes,
}

def app_run():
    while True:
        try:
            print_gui_menu()
            n = input("请选择, q退出:")
            if n == 'q':
                break
            n = int(n)
            menus_handles[n]()
        except Exception as e:
            print(e)

