from data.jpa import jpacompement
from data.jpa.models import ImagesInfos
from hub.docker_registry import DockerRegistryClient
from setting import settings


def load_db_images():
    """
    查看已有数据库中镜像
    :return:
    """
    images_list = jpacompement.JpaImagesInfos.query_list()
    if len(images_list) == 0:
        print('当前没有镜像')
        input('输入任意键退出')
    else:
        print('当前 已有镜像如下：')
        print('序号:\t镜像ID:\t镜像名:\t镜像版本:\t镜像大小:\t')
        for i, image in enumerate(images_list):
            print(f'{i}\t{image.images_id}\t{image.images_name}\t{image.images_version}\t{image.images_size}')

        n = input('输入q退出,输入序号获取完整镜像地址:')
        if not n.count('q'):
            n = int(n)
            images_id = images_list[n].images_id
            hub_registry = settings.hub_registry.hub_registry_url
            if hub_registry.startswith("https://"):
                hub_registry = hub_registry.replace("https://", '')
            if hub_registry.startswith("http://"):
                hub_registry = hub_registry.replace("http://", '')
            if hub_registry.endswith("/"):
                hub_registry = hub_registry[0:-1]
            images_url = f"{hub_registry}/{images_id}"
            print(images_url)
            input('输入任意键退出')

def query_docker_images():
    """
    查询docker主机上的镜像
    :return:
    """
    hub_registry = settings.hub_registry
    client = DockerRegistryClient(hub_registry.hub_registry_url, hub_registry.hub_username, hub_registry.hub_password)
    repos = client.get_all_repositories()
    if repos:
        print('当前 已有镜像库如下：')
        print('序号:\t镜像库名')
        for i, repo in enumerate(repos):
            print(f'{i}\t{repo}')
        n = input('输入q退出,选择序号进入仓库')
        if n != 'q':
            n = int(n)
            target_repo = repos[n]
            print(f'查询仓库:{target_repo} 下的镜像')
            tags = client.get_tags_by_repo(target_repo)
            if tags:
                print('当前 已有镜像如下：')
                print('序号:\t镜像:\t大小:')
                for j, tag in enumerate(tags):
                    manifest, digest = client.get_image_manifest(target_repo, tag)
                    size = 0
                    if manifest:
                        config_size = manifest.get('config', {}).get('size', 0)
                        layers = manifest.get('layers', [])
                        layers_size = sum([l.get('size', 0) for l in layers])
                        size = config_size + layers_size
                        size = size / (1024 * 1024)
                    print(f"{j}\t{target_repo}:{tag}\t{size}MB")
                input('输入任意键退出')
            else:
                print(f"仓库 {target_repo} 无标签或查询失败")
                input('输入任意键退出')
    else:
        print('当前没有镜像库')
        input('输入任意键退出')

def sync_docker_images():
    """
    同步镜像库中的镜像到docker服务器上
    :return:
    """
    hub_registry = settings.hub_registry
    client = DockerRegistryClient(hub_registry.hub_registry_url, hub_registry.hub_username, hub_registry.hub_password)
    repos = client.get_all_repositories()
    if repos:
        print('当前 已有镜像库如下：')
        print('序号:\t镜像库名')
        for i, repo in enumerate(repos):
            print(f'{i}\t{repo}')
        n = input('输入q退出,选择序号进入仓库')
        if n != 'q':
            n = int(n)
            target_repo = repos[n]
            print(f'查询仓库:{target_repo} 下的镜像')
            tags = client.get_tags_by_repo(target_repo)
            if tags:
                print('当前 已有镜像如下：')
                print('序号:\t镜像:\t大小:')
                save_db_data = []
                for j, tag in enumerate(tags):
                    manifest, digest = client.get_image_manifest(target_repo, tag)
                    size = 0
                    if manifest:
                        config_size = manifest.get('config', {}).get('size', 0)
                        layers = manifest.get('layers', [])
                        layers_size = sum([l.get('size', 0) for l in layers])
                        size = config_size + layers_size
                        size = size / (1024 * 1024)
                    print(f"{j}\t{target_repo}:{tag}\t{size:.2f}MB")
                    dt = {"images_id": f"{target_repo}:{tag}", "images_name": f"{target_repo}:{tag}", "images_version": tag, "images_size": f"{size:.2f}MB"}
                    save_db_data.append(ImagesInfos(**dt))

                for save_db_datum in save_db_data:
                    try:
                        data = jpacompement.JpaImagesInfos.query_images_name(save_db_datum.images_name)
                        if data == 0:
                            jpacompement.JpaImagesInfos.add_images_infos(save_db_datum)
                    except Exception as e:
                        pass
                input('输入任意键退出')
            else:
                print(f"仓库 {target_repo} 无标签或查询失败")
                input('输入任意键退出')
    else:
        print('当前没有镜像库')
        input('输入任意键退出')