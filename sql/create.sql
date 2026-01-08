
CREATE TABLE IF NOT EXISTS `agent_server_machine`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(120) NOT NULL COMMENT '名称',
  `host` varchar(255) NOT NULL COMMENT 'host',
  `port` int(11) NOT NULL DEFAULT '22',
  `username` varchar(64) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `private_key` varchar(300) DEFAULT NULL,
  `private_key_password` varchar(300) DEFAULT NULL,
  `remark` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='服务器主机资源';


CREATE TABLE IF NOT EXISTS `agent_nginx_bls_machine`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(120) NOT NULL COMMENT '名称',
  `server_id` bigint(20) DEFAULT NULL,
  `container_machine` varchar(64) DEFAULT NULL,
  `container_id` varchar(255) DEFAULT NULL,
  `command_path` varchar(3000) DEFAULT NULL,
  `command_config_path` varchar(3000) DEFAULT NULL,
  `status` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='nginx 负载主机';


CREATE TABLE IF NOT EXISTS `agent_container_pods`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(120) NOT NULL COMMENT '名称',
  `server_id` bigint(20) DEFAULT NULL,
  `container_id` varchar(300) DEFAULT NULL,
  `command_path` varchar(3000) DEFAULT NULL,
  `images_id` varchar(3000) DEFAULT NULL,
  `images_name` varchar(3000) DEFAULT NULL,
  `status` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='服务容器主机';


CREATE TABLE IF NOT EXISTS `agent_images_infos`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `images_id` varchar(3000) DEFAULT NULL,
  `images_name` varchar(3000) DEFAULT NULL,
  `images_version` varchar(3000) DEFAULT NULL,
  `images_size` varchar(3000) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='镜像信息';


