from abc import ABC, abstractmethod
from enum import Enum

import loguru

from config import config


class LoggerBase(ABC):
    @abstractmethod
    def get_logger(self):
        """method should return logger object."""
        pass


class LogLevel(Enum):
    NOTSET = 0
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50

    def get_int_log_level(self, log_level: str) -> int:
        """
        :param log_level: string log level
        :return: value log_level in integer (10, 20, 30, 40, 50) or 0
        """
        if not isinstance(log_level, str):
            return 0
        
        log_level_dict: dict = {
            "NONSET": self.NOTSET.value,
            "DEBUG": self.DEBUG.value,
            "INFO": self.INFO.value,
            "WARNING": self.WARNING.value,
            "ERROR": self.ERROR.value,
            "CRITICAL": self.CRITICAL.value
            }
        
        return log_level_dict.get(log_level.upper(), 0)
    
    def get_str_log_level(self, log_level: int) -> str:
        """
        :param log_level: int log level
        :return: value log_level in string (DEBUG, INFO, WARNING, ERROR, CRITICAL) or NONSET
        """
        if not isinstance(log_level, int):
            return "NONSET"
        
        log_level_dict: dict = {
            self.NOTSET.value: "NONSET",
            self.DEBUG.value: "DEBUG",
            self.INFO.value: "INFO",
            self.WARNING.value: "WARNING",
            self.ERROR.value: "ERROR",
            self.CRITICAL.value: "CRITICAL"
            }
        
        return log_level_dict.get(log_level, "NONSET")


class Logger(LoggerBase):
    def __init__(self, logger_object) -> None:
        self.logger =  logger_object
        self.log_level = LogLevel
        # self.logger.level = LogLevel.get_str_log_level(logger_settings.log_level)
        self.logger.level = config.log_level
    
    def get_logger(self):
        return self.logger


logger = Logger(loguru.logger)


def get_logger():
    return logger.get_logger()
