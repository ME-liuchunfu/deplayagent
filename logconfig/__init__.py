import logging
import logging.handlers


# ===================== 日志核心配置 =====================
def setup_rotating_log(log_file = "app.log", encoding='utf-8', backupCount=7):
    # 1. 定义日志根对象
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # 日志总级别：DEBUG/INFO/WARNING/ERROR/CRITICAL
    logger.handlers.clear()  # 清空默认handler，防止重复打印日志

    # 2. 定义日志格式（可根据需求修改）
    # 格式说明：时间 - 日志级别 - 模块名 - 行号 - 日志内容
    log_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"  # 时间格式美化
    )

    # 3. 关键：配置【按天滚动+保留7天】的文件处理器
    # 日志主文件名称
    # TimedRotatingFileHandler 核心参数说明
    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=log_file,          # 日志主文件路径/名称
        when='midnight',            # 滚动时机：【每天凌晨0点】切割日志
        interval=1,                 # 滚动间隔：1个when单位 → 1天
        backupCount=backupCount,    # 保留日志文件的数量 → 保留7天
        encoding=encoding,          # 解决中文乱码问题
        delay=False,                # 立即创建日志文件
        utc=False                   # 使用【本地时间】而非UTC时间
    )
    # 切割后的日志文件，文件名后缀添加【日期】而非默认数字（必加，可读性极高）
    file_handler.suffix = "%Y-%m-%d"
    # 过滤掉默认的数字后缀日志文件（只保留日期后缀）
    file_handler.extMatch = r"^\d{4}-\d{2}-\d{2}$"

    # 4. 配置控制台输出（可选，开发调试用，生产可注释）
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 5. 给处理器绑定日志格式
    file_handler.setFormatter(log_formatter)
    console_handler.setFormatter(log_formatter)

    # 6. 把处理器添加到日志对象
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger