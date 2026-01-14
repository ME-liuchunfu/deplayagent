import grpc
from grpc_protos.protos import dockermsg_pb2, dockermsg_pb2_grpc

host = '192.100.29.131'
host = '120.78.228.47'
# host = 'localhost'
# ========== 调用gRPC服务 ==========
def run():
    # 1. 创建gRPC的客户端通道，连接服务端，格式：ip:端口
    # grpc.insecure_channel 表示明文连接，生产环境可用 secure_channel + SSL证书
    with grpc.insecure_channel(f'{host}:6305') as channel:
        # 2. 创建客户端调用对象（Stub），自动生成的类
        stub = dockermsg_pb2_grpc.DockerAgentStub(channel)

        # ========== 一、调用【一元RPC】方法 SayHello ==========
        print("===== 调用一元RPC方法 =====")
        # 构造请求体：用 helloworld_pb2 生成 HelloRequest 对象
        response = pull(stub)
        # response = docker_ps(stub)
        # response = docker_restart(stub)
        # response = images(stub)
        # response = docker_down(stub)
        # response = docker_up(stub)
        # response = docker_rollback(stub)
        print(f"服务端响应: {response}")



def docker_rollback(stub):
    request = dockermsg_pb2.Req_DockerRollBack(work_path='/home/docker/nginx', images_name='nginx:1.27')
    response = stub.container_rollback(request)
    return response


def docker_up(stub):
    request = dockermsg_pb2.Req_DockerUp(work_path='/home/docker/nginx')
    response = stub.container_up(request)
    return response

def docker_down(stub):
    request = dockermsg_pb2.Req_DockerDown(work_path='/home/docker/nginx')
    response = stub.container_down(request)
    return response


def docker_restart(stub):
    request = dockermsg_pb2.Req_DockerRestart(container_id='8cd8783f6f36')
    response = stub.container_restart(request)
    print(f'服务器端重启响应: {response}')

    return docker_ps(stub)


def docker_ps(stub):
    request = dockermsg_pb2.Req_DockerInfo()
    response = stub.container_info(request)
    return response

def images(stub):
    request = dockermsg_pb2.Req_DockerImages()
    response = stub.images(request)
    return response

def pull(stub):
    request = dockermsg_pb2.Req_DockerPull(
        repo_tag='hub-docker.bextai.com/test/redis:7',
        login_url="https://hub-docker.bextai.com",
        username='admin',
        password='hub@Bextai2026'
    )
    # request = dockermsg_pb2.Req_DockerPull(
    #     repo_tag='nginx:1.27',
    # )
    # 像调用本地函数一样调用远程方法，直接得到响应结果
    response = stub.pull_images(request)
    return response
