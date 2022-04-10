"""Contain class for logger handlers and formats"""
import logging
import os

from core.config.variables import EnvironmentVariables


class ApplicationLogger(logging.Logger):
    """Custom logger realisation with file and console handlers"""

    def __init__(self, name: str):
        """
        :param name: logger name
        """
        super().__init__(name)
        self.__set_handlers()

    def __set_handlers(self):
        """Set logger handlers and format"""
        if os.getenv(EnvironmentVariables.APPLICATION_MODE) == EnvironmentVariables.APPLICATION_DEBUG_MODE:
            self.setLevel(logging.DEBUG)
        else:
            self.setLevel(logging.INFO)
        self.addHandler(self.__get_console_handler())

    @classmethod
    def __get_console_handler(cls) -> logging.StreamHandler:
        """Gets log formatted console handler

        :return: log formatted console handler
        """
        console_handler = logging.StreamHandler()
        if os.getenv(EnvironmentVariables.APPLICATION_MODE) == EnvironmentVariables.APPLICATION_DEBUG_MODE:
            console_handler.setLevel(logging.DEBUG)
        else:
            console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            "{asctime:^8} | {levelname:^8} | {module}: {message}", "%H:%M:%S", style="{")
        console_handler.setFormatter(console_format)
        return console_handler


app_logger = ApplicationLogger("app")
