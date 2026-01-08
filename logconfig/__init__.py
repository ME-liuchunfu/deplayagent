import logging
from logging.handlers import RotatingFileHandler
import os
import time
from datetime import datetime, timedelta

def setup_rotating_log(
    log_file="app.log",  # 日志文件名前缀
    max_size=100 * 1024 * 1024,  # 单个文件最大100MB（字节）
    backup_count=30,  # 最大备份文件数（防止文件过多，配合7天清理）
    keep_days=7,  # 保留最近7天的日志
    log_level=logging.INFO  # 日志级别
):
    """
    配置按大小滚动（100MB/文件）+ 按时间清理（7天）的日志
    """
    # 1. 创建日志器（logger）
    logger = logging.getLogger()
    logger.setLevel(log_level)  # 全局日志级别
    logger.handlers.clear()  # 清除默认处理器（避免重复输出）

    # 2. 定义日志格式（包含时间、级别、模块、信息）
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 3. 配置按大小滚动的文件处理器（RotatingFileHandler）
    # 当文件超过 max_size 时，自动创建新文件（命名格式：app.log.1, app.log.2...）
    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=max_size,
        backupCount=backup_count,
        encoding="utf-8",  # 支持中文
        delay=False  # 立即创建文件
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # 4. 配置控制台输出（可选，方便调试）
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 5. 清理超过 keep_days 的过期日志文件
    def clean_expired_logs():
        log_dir = os.path.dirname(os.path.abspath(log_file))  # 日志文件所在目录
        log_prefix = os.path.basename(log_file)  # 日志前缀（如 app.log）
        now = time.time()

        for filename in os.listdir(log_dir):
            # 匹配日志文件（包括主文件 app.log 和备份文件 app.log.1, app.log.2...）
            if filename.startswith(log_prefix):
                file_path = os.path.join(log_dir, filename)
                # 获取文件最后修改时间
                file_mtime = os.path.getmtime(file_path)
                # 计算文件是否过期（当前时间 - 文件修改时间 > keep_days 天）
                if now - file_mtime > keep_days * 24 * 3600:
                    try:
                        os.remove(file_path)
                        logger.info(f"已删除过期日志：{filename}")
                    except Exception as e:
                        logger.error(f"删除过期日志失败：{filename}，错误：{e}")

    # 6. 首次运行时清理一次过期日志
    clean_expired_logs()

    return logger

# ------------------------------
# 使用示例
# ------------------------------
if __name__ == "__main__":
    # 初始化日志配置
    logger = setup_rotating_log(
        log_file="logs/app.log",  # 日志存储在 logs 目录（自动创建，需确保权限）
        max_size=100 * 1024 * 1024,  # 100MB/文件
        backup_count=30,  # 最多保留30个备份文件（防止极端情况下文件过多）
        keep_days=7  # 保留7天
    )

    # 测试日志输出
    logger.debug("调试信息（默认不输出，需将 log_level 设为 DEBUG）")
    logger.info("普通信息日志")
    logger.warning("警告日志")
    logger.error("错误日志")
    logger.critical("严重错误日志")