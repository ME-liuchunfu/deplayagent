import requests
import urllib3
from requests.auth import HTTPBasicAuth

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class DockerRegistryClient:
    def __init__(self, registry_url, username=None, password=None):
        self.registry_url = registry_url
        self.auth = HTTPBasicAuth(username, password) if username and password else None
        self.session = requests.Session()
        # 忽略 HTTPS 证书警告（若 Registry 用自签证书，需开启）
        self.session.verify = False  # 生产环境建议关闭，使用合法证书

    def get_all_repositories(self):
        """
        查询 Registry 中所有镜像仓库（如 test/nginx、my-project/app 等）
        """
        url = f"{self.registry_url}/v2/_catalog"
        try:
            response = self.session.get(url, auth=self.auth, timeout=10)
            response.raise_for_status()  # 抛出 HTTP 错误（如 401/404）
            data = response.json()
            return data.get("repositories", [])
        except requests.exceptions.RequestException as e:
            print(f"查询所有仓库失败：{e}")
            return []

    def get_image_digest(self, repo_name, tag):
        """
        获取镜像的 digest（删除镜像需要用到）
        :param repo_name: 仓库名
        :param tag: 镜像标签
        :return: 镜像 digest 字符串，失败返回 None
        """
        _, digest = self.get_image_manifest(repo_name, tag)
        return digest

    def get_tags_by_repo(self, repo_name):
        """
        查询指定仓库的所有镜像标签（如 test/nginx 的 v1、1.28 等）
        :param repo_name: 仓库名（如 "test/nginx"）
        :return: 标签列表
        """
        url = f"{self.registry_url}/v2/{repo_name}/tags/list"
        try:
            response = self.session.get(url, auth=self.auth, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get("tags", [])
        except requests.exceptions.RequestException as e:
            print(f"查询仓库 {repo_name} 标签失败：{e}")
            return []

    def get_image_manifest(self, repo_name, tag):
        """
        查询指定镜像的详细信息（manifest），包含分层、架构等
        :param repo_name: 仓库名（如 "test/nginx"）
        :param tag: 镜像标签（如 "1.28"）
        :return: 镜像详情字典
        """
        url = f"{self.registry_url}/v2/{repo_name}/manifests/{tag}"
        # 请求头必须指定 manifest 版本（v2），否则返回旧格式
        headers = {
            "Accept": "application/vnd.oci.image.manifest.v1+json, application/vnd.docker.distribution.manifest.v2+json"
        }
        try:
            response = self.session.get(url, headers=headers, auth=self.auth, timeout=10)
            response.raise_for_status()
            return response.json(), response.headers.get('Docker-Content-Digest')
        except requests.exceptions.RequestException as e:
            print(f"查询镜像 {repo_name}:{tag} 详情失败：{e}")
            return {}, None

    def delete_image(self, repo_name, digest):
        """
        删除远程 Registry 中的镜像
        :param repo_name: 仓库名（如 "test/nginx"）
        :param digest: 镜像的 digest（如 "sha256:xxxxxxx"）
        :return: bool - 删除是否成功
        """
        if not digest:
            print("digest 不能为空")
            return False

        url = f"{self.registry_url}/v2/{repo_name}/manifests/{digest}"
        try:
            response = self.session.delete(url, auth=self.auth, timeout=10)
            # 202 Accepted 表示删除请求已接受（异步处理）
            if response.status_code in [202, 200]:
                print(f"镜像 {repo_name}@{digest} 删除请求提交成功")
                return True
            else:
                print(f"删除镜像失败，状态码：{response.status_code}，响应：{response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"删除镜像 {repo_name}@{digest} 失败：{e}")
            return False

    def delete_image_by_tag(self, repo_name, tag):
        """
        通过标签删除镜像（封装 digest 获取和删除操作）
        :param repo_name: 仓库名
        :param tag: 镜像标签
        :return: bool - 删除是否成功
        """
        print(f"正在获取 {repo_name}:{tag} 的 digest...")
        digest = self.get_image_digest(repo_name, tag)
        if not digest:
            print(f"获取 {repo_name}:{tag} 的 digest 失败")
            return False

        print(f"获取到 digest：{digest}")
        print(f"正在删除 {repo_name}:{tag}（{digest}）...")
        return self.delete_image(repo_name, digest)


# -------------------------- 脚本运行示例 --------------------------
if __name__ == "__main__":
    # -------------------------- 配置项（根据你的环境修改） --------------------------
    # Registry 地址（带协议，末尾不加 /）
    REGISTRY_URL = ""
    # Registry 认证信息（无认证则设为 None）
    USERNAME = ""
    PASSWORD = ""
    # ------------------------------------------------------------------------------

    # 初始化客户端
    client = DockerRegistryClient(REGISTRY_URL, USERNAME, PASSWORD)

    # 1. 查询所有镜像仓库
    print("=== 所有镜像仓库 ===")
    repos = client.get_all_repositories()
    if repos:
        for repo in repos:
            print(f"- {repo}")
    else:
        print("无镜像仓库")

    target_repo = "test/redis"
    print(f"\n=== 仓库 {target_repo} 的所有标签 ===")
    tags = client.get_tags_by_repo(target_repo)
    if tags:
        for tag in tags:
            print(f"- {tag}")
    else:
        print(f"仓库 {target_repo} 无标签或查询失败")

    target_tag = "6.2"
    print(f"\n=== 镜像 {target_repo}:{target_tag} 详情 ===")
    manifest, digest = client.get_image_manifest(target_repo, target_tag)
    print(manifest)
    if manifest:
        # 提取关键信息：架构、分层数量、镜像 digest
        print(f"镜像架构：{manifest.get('annotations', {}).get('com.docker.official-images.bashbrew.arch', '未知')}")
        print(f"镜像分层数量：{len(manifest.get('layers', []))}")
        print(f"镜像 Digest：{manifest.get('annotations', {}).get('org.opencontainers.image.base.digest', '未知')}")
        print(f"镜像 Digest：{digest or '未知'}")

    delete_demo = False  # 设置为 True 以执行删除演示
    if delete_demo:
        # 方式1：通过 tag 删除（推荐，更直观）
        delete_success = client.delete_image_by_tag(target_repo, target_tag)
        if delete_success:
            print(f"\n{target_repo}:{target_tag} 删除成功")
        else:
            print(f"\n{target_repo}:{target_tag} 删除失败")