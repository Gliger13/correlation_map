"""Contains variables and config for correlation"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional

import cv2

from correlation_map.gui.core.figure_widgets.image_with_selector_widget import ImageSelectedRegion


class CorrelationTypes(Enum):
    """Represents available correlation types, theis names and contestants in cv2"""

    TM_SQDIFF = "square_difference_correlation", cv2.TM_SQDIFF
    TM_SQDIFF_NORMED = "square_difference_normed_correlation", cv2.TM_SQDIFF_NORMED, True
    TM_CCORR = "cross_correlation", cv2.TM_CCORR
    TM_CCORR_NORMED = "cross_correlation_normed", cv2.TM_CCORR_NORMED
    TM_CCOEFF = "correlation_coefficient", cv2.TM_CCOEFF
    TM_CCOEFF_NORMED = "correlation_coefficient_normed", cv2.TM_CCOEFF_NORMED

    def __init__(self, correlation_type: str, correlation_cv2_type: int, is_default: bool = False):
        """
        :param correlation_type: correlation type name
        :param correlation_cv2_type: correlation constant in cv2
        :param is_default: True if it's default correlation type else False
        """
        self.correlation_type = correlation_type
        self.correlation_cv2_type = correlation_cv2_type
        self.is_default = is_default


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


@dataclass(kw_only=True)
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
