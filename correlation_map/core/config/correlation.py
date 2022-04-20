"""Contains variables and config for correlation"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from correlation_map.core.correlation.correlation_maker import CorrelationTypes
from correlation_map.gui.core.image_widget import ImageSelectedRegion


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


@dataclass
class CorrelationConfiguration:
    """Contains correlation configuration for building correlation map"""
    # Preprocessor actions
    auto_rotate: bool = False
    auto_find: bool = False
    chose_important_part: bool = False

    correlation_type: CorrelationTypes = CorrelationTypes.TM_SQDIFF_NORMED

    # Auto rotate configuration
    detection_match_count: int = CorrelationSettings.DETECTION_MATCH_COUNT.default_value
    # Correlation configuration
    correlation_pieces_count: int = CorrelationSettings.CORRELATION_PIECES_COUNT.default_value

    # Chose important part configuration
    selected_image_region: Optional[ImageSelectedRegion] = None
