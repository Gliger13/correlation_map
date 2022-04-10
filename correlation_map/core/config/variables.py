"""Contains classes for environment variables and a function to check required environment variables"""
import os
from enum import Enum
from typing import Iterable, Optional

from core.errors.common import EnvironmentVariablesError, MissedEnvironmentVariableError, \
    WrongEnvironmentVariableError


class EnvironmentVariables:
    """Contains all environment variable and their expected values if they have"""

    APPLICATION_DEBUG_MODE = "DEBUG"
    APPLICATION_PROD_MODE = "PROD"


class RequiredEnvironmentVariables(Enum):
    """Contains all required environment variables and their expected values if they have"""

    APPLICATION_MODE = "MODE", (EnvironmentVariables.APPLICATION_DEBUG_MODE, EnvironmentVariables.APPLICATION_PROD_MODE)

    def __init__(self, variable: str, possible_values: Optional[Iterable[str]] = None):
        """
        :param variable: required environment variable name
        :param possible_values: expected environment variable values
        """
        self.variable = variable
        self.possible_values = possible_values


def check_required_environment_variables():
    """Check environment variables for required

    :raise EnvironmentVariablesError: if there is more than one environment variable errors
    :raise MissedEnvironmentVariableError: if a required environment variable missed
    :raise WrongEnvironmentVariableError: if an environment variable has the wrong value
    """
    errors: list[EnvironmentVariablesError] = []

    for required_environment_variable in RequiredEnvironmentVariables:
        environment_variable_value = os.getenv(required_environment_variable.variable)
        if not environment_variable_value:
            errors.append(MissedEnvironmentVariableError(
                required_environment_variable.variable, required_environment_variable.possible_values))
            continue
        if environment_variable_value not in required_environment_variable.possible_values:
            errors.append(WrongEnvironmentVariableError(
                required_environment_variable.variable, environment_variable_value,
                required_environment_variable.possible_values))

    if errors:
        if len(errors) == 1:
            raise errors[0]
        error_message = "\n".join([f"- {error.short_message}" for error in errors])
        raise EnvironmentVariablesError(error_message)
