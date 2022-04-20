"""Contain class for logger handlers and formats"""
import logging
import os

from correlation_map.core.config.variables import EnvironmentVariables


class ApplicationLogger(logging.Logger):
    """Custom logger realisation with file and console handlers"""

    def __init__(self, name: str):
        """
        :param name: logger name
        """
        super().__init__(name)
        self.__set_handlers()

    @classmethod
    def get_logging_console_formatter(cls) -> logging.Formatter:
        """Return console logging formatter"""
        return logging.Formatter("{asctime:^8} | {levelname:^8} | {module}: {message}", "%H:%M:%S", style="{")

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
        console_handler.setFormatter(cls.get_logging_console_formatter())
        return console_handler


class ToolsLogger(ApplicationLogger):
    """Custom logger realisation with more informal logger"""

    @classmethod
    def get_logging_console_formatter(cls) -> logging.Formatter:
        """Return console logging formatter without module name"""
        return logging.Formatter("{asctime:^8} | {levelname:^8} | {message}", "%H:%M:%S", style="{")


app_logger = ApplicationLogger("app")
tools_logger = ToolsLogger("tools")
