"""Contains classes with constant project variables"""
from enum import Enum
from typing import Iterable, Optional


class EnvironmentVariables:
    """Contains all environment variable and their expected values if they have"""

    APPLICATION_MODE = "MODE"
    APPLICATION_DEBUG_MODE = "DEBUG"
    APPLICATION_PROD_MODE = "PROD"


class RequiredEnvironmentVariables(Enum):
    """Contains all required environment variables and their expected values if they have"""

    APPLICATION_MODE = EnvironmentVariables.APPLICATION_MODE, \
        (EnvironmentVariables.APPLICATION_DEBUG_MODE, EnvironmentVariables.APPLICATION_PROD_MODE)

    def __init__(self, variable: str, possible_values: Optional[Iterable[str]] = None):
        """
        :param variable: required environment variable name
        :param possible_values: expected environment variable values
        """
        self.variable = variable
        self.possible_values = possible_values


class ProjectFileMapping:
    """Contain main project directories and files names"""

    ROOT_DIR_NAME = "correlation_map"
    STATIC_FILES_DIR_NAME = "static"
    EXCLUDED_DIRS = {"venv", ".idea", "__pycache__"}

    RUN_ICON_FILE_NAME = "run_icon.png"
    STOP_ICON_FILE_NAME = "stop_icon.png"
    TERMINATE_ICON_FILE_NAME = "terminate_icon.png"
