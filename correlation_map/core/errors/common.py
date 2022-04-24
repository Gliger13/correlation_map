"""Contains custom project error classes"""
from typing import Iterable, Optional


class EnvironmentVariablesError(Exception):
    """Error when there are problems with environment variables"""

    def __init__(self, message_error: Optional[str] = None):
        """
        :param message_error: optional additional error message
        """
        super().__init__()
        self.message_error = message_error

    @property
    def short_message(self) -> str:
        """Returns short error message"""
        return "Incorrect environment variables specified"

    @property
    def message(self) -> str:
        """Returns full error message"""
        if self.message_error:
            return f"{self.short_message}\n{self.message_error}"
        return self.short_message

    def __str__(self) -> str:
        """Error message while raising"""
        return self.message


class MissedEnvironmentVariableError(EnvironmentVariablesError):
    """Error when environment variable is missed"""

    def __init__(self, variable_name: str, possible_values: Optional[Iterable[str]] = None):
        """
        :param variable_name: name of the missed environment variable
        :param possible_values: iterable of expected environment variable values
        """
        super().__init__()
        self.variable_name = variable_name
        self.possible_values = possible_values

    @property
    def short_message(self) -> str:
        """Returns short error message"""
        general_message = f"Missed required environment variable `{self.variable_name}`"
        if self.possible_values:
            expected_values_message = ", ".join(self.possible_values)
            general_message = f"{general_message}. Expected any of ({expected_values_message})"
        return general_message

    @property
    def message(self) -> str:
        """Returns full error message"""
        return f"Missed environment variable `{self.variable_name}`\n{self.short_message}"


class WrongEnvironmentVariableError(EnvironmentVariablesError):
    """Error when environment variable has wrong value"""

    def __init__(self, variable_name: str, wrong_value: str, possible_values: Iterable[str]):
        """
        :param variable_name: name of the wrong environment variable
        :param wrong_value: value of the wrong environment variable
        :param possible_values: iterable of expected environment variable values
        """
        super().__init__()
        self.variable_name = variable_name
        self.wrong_value = wrong_value
        self.possible_values = possible_values

    @property
    def short_message(self) -> str:
        """Returns short error message"""
        expected_values_message = ", ".join(self.possible_values)
        return f"Incorrect environment variable value for `{self.variable_name}`: got `{self.wrong_value}`, " \
               f"expected any of ({expected_values_message})"

    @property
    def message(self) -> str:
        """Returns full error message"""
        return f"Wrong environment variable value of `{self.variable_name}`\n{self.short_message}"
