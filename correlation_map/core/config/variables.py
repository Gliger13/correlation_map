"""Contains classes for environment variables"""
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
