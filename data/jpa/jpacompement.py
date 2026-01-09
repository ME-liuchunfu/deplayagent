"""
db操作组件
"""
import logging
from typing import List, Optional
from data.jpa.models import ServerMachine, NginxBlsMachine, ContainerPods, ImagesInfos, NginxBlsWeight, \
    ContainerPodsVersion
from setting import settings
from data.jpa import base as db_base


logger = logging.getLogger(__name__)


class JpaServerMachine:

    @classmethod
    def query_list(cls) -> List[ServerMachine]:
        datas = []
        conn = db_base.connect_to_mysql(settings.database)
        try:
            with conn.cursor() as cursor:
                cursor.execute("select * from agent_server_machine")
                db_rows = cursor.fetchall()
                if db_rows and len(db_rows) > 0:
                    for row in db_rows:
                        datas.append(ServerMachine(**row))
        except Exception as e:
            logger.error(f"查询主机信息错误", exc_info=True)
        finally:
            db_base.close(conn)
        return datas

    @classmethod
    def add_machine(cls, server_machine: ServerMachine):
        conn = db_base.connect_to_mysql(settings.database)
        try:
            logger.info(f"插入主机信息:{server_machine.__dict__}")
            with conn.cursor() as cursor:
                query = """
                insert into agent_server_machine(`name`, `host`, `port`, `username`, `password`, `private_key`, `private_key_password`, `remark`)
                values(%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    server_machine.name,
                    server_machine.host,
                    server_machine.port,
                    server_machine.username,
                    server_machine.password,
                    server_machine.private_key,
                    server_machine.private_key_password,
                    server_machine.remark
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"插入主机信息错误:{server_machine.__dict__}", exc_info=True)
        finally:
            db_base.close(conn)

    @classmethod
    def del_machine(cls, id: int):
        conn = db_base.connect_to_mysql(settings.database)
        try:
            logger.info(f"删除主机信息id:{id}")
            with conn.cursor() as cursor:
                cursor.execute("delete from agent_server_machine where id = %s", id)
                conn.commit()
        except Exception as e:
            logger.error(f"删除主机信息错误 id:{id}", exc_info=True)
        finally:
            db_base.close(conn)

    @classmethod
    def update_machine(cls, server_machine: ServerMachine):
        conn = db_base.connect_to_mysql(settings.database)
        try:
            logger.info(f"更新主机信息:{server_machine.__dict__}")
            with conn.cursor() as cursor:
                query = """
                update agent_server_machine 
                set `name`=%s, `host`=%s, `port`=%s, `username`=%s, `password`=%s,
                    `private_key`=%s, `private_key_password`=%s, `remark`=%s
                where
                    id = %s
                """
                cursor.execute(query, (
                    server_machine.name,
                    server_machine.host,
                    server_machine.port,
                    server_machine.username,
                    server_machine.password,
                    server_machine.private_key,
                    server_machine.private_key_password,
                    server_machine.remark,
                    server_machine.id
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"更新主机信息错误:{server_machine.__dict__}", exc_info=True)
        finally:
            db_base.close(conn)

    @classmethod
    def query_by_id(cls, server_id) -> Optional[ServerMachine]:
        conn = db_base.connect_to_mysql(settings.database)
        try:
            data = None
            logger.info(f"查询主机信息:{server_id}")
            with conn.cursor() as cursor:
                cursor.execute("select * from agent_server_machine where id = %s", server_id)
                row = cursor.fetchone()
                if row:
                    data = ServerMachine(**row)
            return data
        except Exception as e:
            pass
        finally:
            db_base.close(conn)
        return None


class JpaNginxBlsMachine:

    @classmethod
    def query_list(cls) -> List[NginxBlsMachine]:
        datas = []
        conn = db_base.connect_to_mysql(settings.database)
        try:
            with conn.cursor() as cursor:
                cursor.execute("select * from agent_nginx_bls_machine")
                db_rows = cursor.fetchall()
                if db_rows and len(db_rows) > 0:
                    for row in db_rows:
                        datas.append(NginxBlsMachine(**row))
        except Exception as e:
            logger.error(f"查询nginx bls主机信息错误", exc_info=True)
        finally:
            db_base.close(conn)
        return datas

    @classmethod
    def add_nginx_bls_machine(cls, nginx_bls_machine: NginxBlsMachine):
        conn = db_base.connect_to_mysql(settings.database)
        try:
            logger.info(f"插入nginx bls主机信息:{nginx_bls_machine.__dict__}")
            with conn.cursor() as cursor:
                query = """
                insert into agent_nginx_bls_machine(`name`, `server_id`, `container_machine`, 
                    `container_id`, `command_path`, `command_config_path`, `status`)
                values(%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    nginx_bls_machine.name,
                    nginx_bls_machine.server_id,
                    nginx_bls_machine.container_machine,
                    nginx_bls_machine.container_id,
                    nginx_bls_machine.command_path,
                    nginx_bls_machine.command_config_path,
                    nginx_bls_machine.status
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"插入nginx bls主机信息错误:{nginx_bls_machine.__dict__}", exc_info=True)
        finally:
            db_base.close(conn)

    @classmethod
    def del_nginx_bls_machine(cls, id: int):
        conn = db_base.connect_to_mysql(settings.database)
        try:
            logger.info(f"删除nginx bls主机信息id:{id}")
            with conn.cursor() as cursor:
                cursor.execute("delete from agent_nginx_bls_machine where id = %s", id)
                conn.commit()
        except Exception as e:
            logger.error(f"删除nginx bls主机信息错误 id:{id}", exc_info=True)
        finally:
            db_base.close(conn)

    @classmethod
    def update_nginx_bls_machine(cls, nginx_bls_machine: NginxBlsMachine):
        conn = db_base.connect_to_mysql(settings.database)
        try:
            logger.info(f"更新nginx bls主机信息:{nginx_bls_machine.__dict__}")
            with conn.cursor() as cursor:
                query = """
                update agent_nginx_bls_machine 
                set `name`=%s, `server_id`=%s, `container_machine`=%s, 
                    `container_id`=%s, `command_path`=%s, `command_config_path`=%s, `status`=%s
                where
                    id = %s
                """
                cursor.execute(query, (
                    nginx_bls_machine.name,
                    nginx_bls_machine.server_id,
                    nginx_bls_machine.container_machine,
                    nginx_bls_machine.container_id,
                    nginx_bls_machine.command_path,
                    nginx_bls_machine.command_config_path,
                    nginx_bls_machine.status,
                    nginx_bls_machine.id
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"更新nginx bls主机信息错误:{nginx_bls_machine.__dict__}", exc_info=True)
        finally:
            db_base.close(conn)


class JpaNginxBlsWeight:

    @classmethod
    def query_list(cls) -> List[NginxBlsWeight]:
        datas = []
        conn = db_base.connect_to_mysql(settings.database)
        try:
            with conn.cursor() as cursor:
                cursor.execute("select * from agent_nginx_bls_weight")
                db_rows = cursor.fetchall()
                if db_rows and len(db_rows) > 0:
                    for row in db_rows:
                        datas.append(NginxBlsWeight(**row))
        except Exception as e:
            logger.error(f"查询nginx bls负载项信息错误", exc_info=True)
        finally:
            db_base.close(conn)
        return datas

    @classmethod
    def add_nginx_bls_weight(cls, nginx_bls_weight: NginxBlsWeight):
        conn = db_base.connect_to_mysql(settings.database)
        try:
            logger.info(f"插入nginx bls负载项信息:{nginx_bls_weight.__dict__}")
            with conn.cursor() as cursor:
                query = """
                insert into agent_nginx_bls_weight(`name`, `bls_machine_id`, `command_config_path`, `status`)
                values(%s, %s, %s, %s)
                """
                cursor.execute(query, (
                    nginx_bls_weight.name,
                    nginx_bls_weight.bls_machine_id,
                    nginx_bls_weight.command_config_path,
                    nginx_bls_weight.status
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"插入nginx bls负载项信息错误:{nginx_bls_weight.__dict__}", exc_info=True)
        finally:
            db_base.close(conn)

    @classmethod
    def del_nginx_bls_weight(cls, id: int):
        conn = db_base.connect_to_mysql(settings.database)
        try:
            logger.info(f"删除nginx bls负载项信息id:{id}")
            with conn.cursor() as cursor:
                cursor.execute("delete from agent_nginx_bls_weight where id = %s", id)
                conn.commit()
        except Exception as e:
            logger.error(f"删除nginx bls负载项信息错误 id:{id}", exc_info=True)
        finally:
            db_base.close(conn)

    @classmethod
    def update_nginx_bls_weight(cls, nginx_bls_weight: NginxBlsWeight):
        conn = db_base.connect_to_mysql(settings.database)
        try:
            logger.info(f"更新nginx bls负载项信息:{nginx_bls_weight.__dict__}")
            with conn.cursor() as cursor:
                query = """
                update agent_nginx_bls_weight 
                set `name`=%s, `bls_machine_id`=%s, `command_config_path`=%s, `status`=%s
                where
                    id = %s
                """
                cursor.execute(query, (
                    nginx_bls_weight.name,
                    nginx_bls_weight.bls_machine_id,
                    nginx_bls_weight.command_config_path,
                    nginx_bls_weight.status,
                    nginx_bls_weight.id
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"更新nginx bls负载项信息错误:{nginx_bls_weight.__dict__}", exc_info=True)
        finally:
            db_base.close(conn)

    @classmethod
    def query_list_by_bls_machine_id(cls, bls_id) -> List[NginxBlsWeight]:
        datas = []
        conn = db_base.connect_to_mysql(settings.database)
        try:
            with conn.cursor() as cursor:
                cursor.execute("select * from agent_nginx_bls_weight where bls_machine_id = %s", bls_id)
                db_rows = cursor.fetchall()
                if db_rows and len(db_rows) > 0:
                    for row in db_rows:
                        datas.append(NginxBlsWeight(**row))
        except Exception as e:
            logger.error(f"查询nginx bls负载项信息错误", exc_info=True)
        finally:
            db_base.close(conn)
        return datas


class JpaContainerPods:

    @classmethod
    def query_list(cls) -> List[ContainerPods]:
        datas = []
        conn = db_base.connect_to_mysql(settings.database)
        try:
            with conn.cursor() as cursor:
                cursor.execute("select * from agent_container_pods")
                db_rows = cursor.fetchall()
                if db_rows and len(db_rows) > 0:
                    for row in db_rows:
                        datas.append(ContainerPods(**row))
        except Exception as e:
            logger.error(f"查询服务容器主机信息错误", exc_info=True)
        finally:
            db_base.close(conn)
        return datas

    @classmethod
    def add_container_pods(cls, container_pods: ContainerPods):
        conn = db_base.connect_to_mysql(settings.database)
        try:
            logger.info(f"插入服务容器主机信息:{container_pods.__dict__}")
            with conn.cursor() as cursor:
                query = """
                insert into agent_container_pods(`name`, `server_id`, `container_id`, 
                    `command_path`, `images_id`, `images_name`, `status`)
                values(%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    container_pods.name,
                    container_pods.server_id,
                    container_pods.container_id,
                    container_pods.command_path,
                    container_pods.images_id,
                    container_pods.images_name,
                    container_pods.status
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"插入服务容器主机信息错误:{container_pods.__dict__}", exc_info=True)
        finally:
            db_base.close(conn)

    @classmethod
    def del_container_pods(cls, id: int):
        conn = db_base.connect_to_mysql(settings.database)
        try:
            logger.info(f"删除服务容器主机信息id:{id}")
            with conn.cursor() as cursor:
                cursor.execute("delete from agent_container_pods where id = %s", id)
                conn.commit()
        except Exception as e:
            logger.error(f"删除服务容器主机信息错误 id:{id}", exc_info=True)
        finally:
            db_base.close(conn)

    @classmethod
    def update_container_pods(cls, container_pods: ContainerPods):
        conn = db_base.connect_to_mysql(settings.database)
        try:
            logger.info(f"更新服务容器主机信息:{container_pods.__dict__}")
            with conn.cursor() as cursor:
                query = """
                update agent_container_pods 
                set `name`=%s, `server_id`=%s, `container_id`=%s, 
                    `command_path`=%s, `images_id`=%s, `images_name`=%s, `status`=%s
                where
                    id = %s
                """
                cursor.execute(query, (
                    container_pods.name,
                    container_pods.server_id,
                    container_pods.container_id,
                    container_pods.command_path,
                    container_pods.images_id,
                    container_pods.images_name,
                    container_pods.status,
                    container_pods.id
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"更新服务容器主机信息错误:{container_pods.__dict__}", exc_info=True)
        finally:
            db_base.close(conn)

    @classmethod
    def query_list_by_machine_id(cls, server_id)->List[ContainerPods]:
        datas = []
        conn = db_base.connect_to_mysql(settings.database)
        try:
            with conn.cursor() as cursor:
                cursor.execute("select * from agent_container_pods where server_id=%s", server_id)
                db_rows = cursor.fetchall()
                if db_rows and len(db_rows) > 0:
                    for row in db_rows:
                        datas.append(ContainerPods(**row))
        except Exception as e:
            logger.error(f"查询服务容器主机信息错误", exc_info=True)
        finally:
            db_base.close(conn)
        return datas


class JpaContainerPodsVersion:

    @classmethod
    def query_list(cls) -> List[ContainerPodsVersion]:
        datas = []
        conn = db_base.connect_to_mysql(settings.database)
        try:
            with conn.cursor() as cursor:
                cursor.execute("select * from agent_container_pods_version")
                db_rows = cursor.fetchall()
                if db_rows and len(db_rows) > 0:
                    for row in db_rows:
                        datas.append(ContainerPodsVersion(**row))
        except Exception as e:
            logger.error(f"查询服务容器版本信息错误", exc_info=True)
        finally:
            db_base.close(conn)
        return datas

    @classmethod
    def add_container_pods_version(cls, container_pods_version: ContainerPodsVersion):
        conn = db_base.connect_to_mysql(settings.database)
        try:
            logger.info(f"插入服务容器版本信息:{container_pods_version.__dict__}")
            with conn.cursor() as cursor:
                query = """
                insert into agent_container_pods_version(`name`, `server_id`, `pods_id`, 
                    `command_path`, `images_id`, `images_name`)
                values(%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    container_pods_version.name,
                    container_pods_version.server_id,
                    container_pods_version.pods_id,
                    container_pods_version.command_path,
                    container_pods_version.images_id,
                    container_pods_version.images_name
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"插入服务容器版本信息错误:{container_pods_version.__dict__}", exc_info=True)
        finally:
            db_base.close(conn)

    @classmethod
    def del_container_pods_version(cls, id: int):
        conn = db_base.connect_to_mysql(settings.database)
        try:
            logger.info(f"删除服务容器版本信息id:{id}")
            with conn.cursor() as cursor:
                cursor.execute("delete from agent_container_pods_version where id = %s", id)
                conn.commit()
        except Exception as e:
            logger.error(f"删除服务容器版本信息错误 id:{id}", exc_info=True)
        finally:
            db_base.close(conn)

    @classmethod
    def update_container_pods_version(cls, container_pods_version: ContainerPodsVersion):
        conn = db_base.connect_to_mysql(settings.database)
        try:
            logger.info(f"更新服务容器版本信息:{container_pods_version.__dict__}")
            with conn.cursor() as cursor:
                query = """
                update agent_container_pods_version
                set `name`=%s, `server_id`=%s, `pods_id`=%s, 
                    `command_path`=%s, `images_id`=%s, `images_name`=%s
                where
                    id = %s
                """
                cursor.execute(query, (
                    container_pods_version.name,
                    container_pods_version.server_id,
                    container_pods_version.pods_id,
                    container_pods_version.command_path,
                    container_pods_version.images_id,
                    container_pods_version.images_name,
                    container_pods_version.id
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"更新服务容器版本信息错误:{container_pods_version.__dict__}", exc_info=True)
        finally:
            db_base.close(conn)

    @classmethod
    def query_pods_version_by_pods_id(cls, pod_id) -> List[ContainerPodsVersion]:
        datas = []
        conn = db_base.connect_to_mysql(settings.database)
        try:
            with conn.cursor() as cursor:
                cursor.execute("select * from agent_container_pods_version where pods_id=%s limit 10", pod_id)
                db_rows = cursor.fetchall()
                if db_rows and len(db_rows) > 0:
                    for row in db_rows:
                        datas.append(ContainerPodsVersion(**row))
        except Exception as e:
            logger.error(f"查询服务容器版本信息错误", exc_info=True)
        finally:
            db_base.close(conn)
        return datas


class JpaImagesInfos:

    @classmethod
    def query_list(cls) -> List[ImagesInfos]:
        datas = []
        conn = db_base.connect_to_mysql(settings.database)
        try:
            with conn.cursor() as cursor:
                cursor.execute("select * from agent_images_infos")
                db_rows = cursor.fetchall()
                if db_rows and len(db_rows) > 0:
                    for row in db_rows:
                        datas.append(ImagesInfos(**row))
        except Exception as e:
            logger.error(f"查询镜像信息主机信息错误", exc_info=True)
        finally:
            db_base.close(conn)
        return datas

    @classmethod
    def add_images_infos(cls, images_infos: ImagesInfos):
        conn = db_base.connect_to_mysql(settings.database)
        try:
            logger.info(f"插入镜像信息主机信息:{images_infos.__dict__}")
            with conn.cursor() as cursor:
                query = """
                insert into agent_images_infos(`images_id`, `images_name`, `images_version`,  `images_size`)
                values(%s, %s, %s, %s)
                """
                cursor.execute(query, (
                    images_infos.images_id,
                    images_infos.images_name,
                    images_infos.images_version,
                    images_infos.images_size
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"插入镜像信息主机信息错误:{images_infos.__dict__}", exc_info=True)
        finally:
            db_base.close(conn)

    @classmethod
    def del_images_infos(cls, id: int):
        conn = db_base.connect_to_mysql(settings.database)
        try:
            logger.info(f"删除镜像信息主机信息id:{id}")
            with conn.cursor() as cursor:
                cursor.execute("delete from agent_images_infos where id = %s", id)
                conn.commit()
        except Exception as e:
            logger.error(f"删除镜像信息主机信息错误 id:{id}", exc_info=True)
        finally:
            db_base.close(conn)

    @classmethod
    def update_images_infos(cls, images_infos: ImagesInfos):
        conn = db_base.connect_to_mysql(settings.database)
        try:
            logger.info(f"更新镜像信息主机信息:{images_infos.__dict__}")
            with conn.cursor() as cursor:
                query = """
                update agent_images_infos 
                set `images_id`=%s, `images_name`=%s, `images_version`=%s, `images_size`=%s
                where
                    id = %s
                """
                cursor.execute(query, (
                    images_infos.images_id,
                    images_infos.images_name,
                    images_infos.images_version,
                    images_infos.images_size,
                    images_infos.id
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"更新镜像信息主机信息错误:{images_infos.__dict__}", exc_info=True)
        finally:
            db_base.close(conn)

    @classmethod
    def query_images_name(cls, images_name: str):
        conn = db_base.connect_to_mysql(settings.database)
        size = 0
        try:
            with conn.cursor() as cursor:
                cursor.execute("select * from agent_images_infos where images_name=%s", images_name)
                db_rows = cursor.fetchall()
                if db_rows and len(db_rows) > 0:
                    size = 1
        except Exception as e:
            logger.error(f"查询镜像信息主机信息错误", exc_info=True)
        finally:
            db_base.close(conn)
        return size
