"""
db操作组件
"""
import logging
from typing import List
from data.jpa.models import ServerMachine, NginxBlsMachine, ContainerPods, ImagesInfos
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
            logger.error(f"查询主机信息错误", e)
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
            logger.error(f"插入主机信息错误:{server_machine.__dict__}", e)
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
            logger.error(f"删除主机信息错误 id:{id}", e)
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
            logger.error(f"更新主机信息错误:{server_machine.__dict__}", e)
        finally:
            db_base.close(conn)



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
            logger.error(f"查询nginx bls主机信息错误", e)
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
            logger.error(f"插入nginx bls主机信息错误:{nginx_bls_machine.__dict__}", e)
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
            logger.error(f"删除nginx bls主机信息错误 id:{id}", e)
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
            logger.error(f"更新nginx bls主机信息错误:{nginx_bls_machine.__dict__}", e)
        finally:
            db_base.close(conn)



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
            logger.error(f"查询服务容器主机信息错误", e)
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
            logger.error(f"插入服务容器主机信息错误:{container_pods.__dict__}", e)
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
            logger.error(f"删除服务容器主机信息错误 id:{id}", e)
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
            logger.error(f"更新服务容器主机信息错误:{container_pods.__dict__}", e)
        finally:
            db_base.close(conn)


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
            logger.error(f"查询镜像信息主机信息错误", e)
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
            logger.error(f"插入镜像信息主机信息错误:{images_infos.__dict__}", e)
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
            logger.error(f"删除镜像信息主机信息错误 id:{id}", e)
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
            logger.error(f"更新镜像信息主机信息错误:{images_infos.__dict__}", e)
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
            logger.error(f"查询镜像信息主机信息错误", e)
        finally:
            db_base.close(conn)
        return size
