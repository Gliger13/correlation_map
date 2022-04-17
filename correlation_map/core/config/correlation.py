"""Contains variables and config for correlation"""
from enum import Enum


class PreprocessorActions(Enum):
    """Contains all available preprocessor actions"""

    AUTO_ROTATION = "auto rotation"
    AUTO_FIND = "auto find"
    CHOSE_IMPORTANT_PART = "chose important part"


class CorrelationSettings(Enum):
    """Contains all available correlation settings"""

    DETECTION_MATCH_COUNT = "detections match amount", 5
    CORRELATION_PIECES_COUNT = "correlation pieces amount", 2

    def __init__(self, setting: str, default_value: int):
        """
        :param setting: setting name
        :param default_value: default value for the setting
        """
        self.setting = setting
        self.default_value = default_value
