import logging
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from data.asyncl.mysql_data import init_setup
from data.asyncl.mysql_orm import DockerServer
from hub.docker_registry import DockerRegistryClient
from web import resp_fail, resp_ok


logger = logging.getLogger(__name__)

router = APIRouter()


async def query_hub(hub_id: int, db: AsyncSession) -> Optional[DockerServer]:
    sql = select(DockerServer).filter(DockerServer.id == hub_id)
    qb = await db.execute(sql)
    data = qb.scalar_one_or_none()
    if data is None:
        raise ValueError('找不到镜像服务')
    return data


@router.get("/repositories/all/{hub_id}")
async def all_repositories(hub_id: int, db: AsyncSession = Depends(init_setup.get_async_db)):
    data = await query_hub(hub_id, db)
    domain = data.domain
    if domain.endswith('/'):
        domain = domain[0:-1]
    pull_domain = domain
    if pull_domain.startswith('https://'):
        pull_domain = pull_domain.replace('https://', '')
    if pull_domain.startswith('http://'):
        pull_domain = pull_domain.replace('http://', '')
    registry_client = DockerRegistryClient(
        registry_url=domain,
        username=data.username,
        password=data.passwd
    )
    datas = registry_client.get_all_repositories()
    result_datas = []
    if datas and len(datas) > 0:
        for repo in datas:
            try:
                item = {
                    "domain": data.domain,
                    "name": data.name,
                    "repo": repo,
                    "tags": []
                }
                result_datas.append(item)
                versions = registry_client.get_tags_by_repo(repo)
                if versions and len(versions) > 0:
                    for version in versions:
                        try:
                            image_size = '0MB'
                            manifest, digest = registry_client.get_image_manifest(repo, version)
                            if manifest:
                                config_size = manifest.get('config', {}).get('size', 0)
                                layers = manifest.get('layers', [])
                                layers_size = sum([l.get('size', 0) for l in layers])
                                size = config_size + layers_size
                                size = size / (1024 * 1024)
                                image_size = f'{size:.4f}MB'
                            item.get("tags").append({
                                "version": f"{repo}:{version}",
                                "pull_url": f"{pull_domain}/{repo}:{version}",
                                "size": image_size
                            })
                        except Exception as ex:
                            logger.error(f'hub查询错误{data},repo:{repo}', exc_info=True)
            except Exception as e:
                logger.error(f'hub查询错误{data}', exc_info=True)
    return resp_ok(data=result_datas)


@router.get("/repositories/query/{hub_id}")
async def all_repositories(hub_id: int, db: AsyncSession = Depends(init_setup.get_async_db)):
    data = await query_hub(hub_id, db)
    domain = data.domain
    if domain.endswith('/'):
        domain = domain[0:-1]
    registry_client = DockerRegistryClient(
        registry_url=domain,
        username=data.username,
        password=data.passwd
    )
    datas = registry_client.get_all_repositories()
    return resp_ok(data=datas)


@router.get("/repositories/tags/{hub_id}")
async def tags_repo(hub_id: int, repo: str, db: AsyncSession = Depends(init_setup.get_async_db)):
    if repo is None:
        return resp_fail(msg='缺失仓库')
    data = await query_hub(hub_id, db)
    domain = data.domain
    if domain.endswith('/'):
        domain = domain[0:-1]
    registry_client = DockerRegistryClient(
        registry_url=domain,
        username=data.username,
        password=data.passwd
    )
    datas = registry_client.get_tags_by_repo(repo)
    return resp_ok(data=datas)

