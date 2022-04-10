"""Contains a function to check required environment variables"""
import os

from core.config.variables import RequiredEnvironmentVariables
from core.errors.common import EnvironmentVariablesError, MissedEnvironmentVariableError, WrongEnvironmentVariableError
from gui.tools.logger import app_logger


def check_required_environment_variables():
    """Check environment variables for required

    :raise EnvironmentVariablesError: if there is more than one environment variable errors
    :raise MissedEnvironmentVariableError: if a required environment variable missed
    :raise WrongEnvironmentVariableError: if an environment variable has the wrong value
    """
    app_logger.debug("Checking environment variables")
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
    app_logger.debug("No environment variable issues found")
