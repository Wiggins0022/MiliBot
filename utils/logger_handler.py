import logging
import os
from datetime import datetime

class LoggerHandler:
    def __init__(self,log_dir: str='logs'):
        """
        :param log_dir: 日志保存的根目录
        """
        self.LOG_DIR = log_dir

        os.makedirs(self.LOG_DIR, exist_ok=True)

        self.DEFAULT_LOG_FORMAT = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s -%(filename)s:%(lineno)d - %(message)s'
        )

    def get_logger(
            self,
            name: str = "agent_logger",
            console_level: int = logging.INFO,
            file_level: int = logging.DEBUG,
            log_file: str = None) -> logging.Logger:
        """
            获取配置好的日志记录器
        :param name: 日志记录器的名称
        :param console_level: 控制台日志级别
        :param file_level: 文件日志级别
        :param log_file: 日志文件路径
        :return:配置好的日志记录器
        """
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)  # 设置最低日志级别为DEBUG

        # 避免重复添加Handler
        if logger.handlers:
            return logger

        # 添加控制台Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(console_level)
        console_handler.setFormatter(self.DEFAULT_LOG_FORMAT)
        logger.addHandler(console_handler)

        # 添加文件Handler
        if not log_file:
            log_file = os.path.join(self.LOG_DIR, f"{name}_{datetime.now().strftime('%Y%m%d')}.log")

        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(file_level)
        file_handler.setFormatter(self.DEFAULT_LOG_FORMAT)
        logger.addHandler(file_handler)

        return logger

logger = LoggerHandler().get_logger()