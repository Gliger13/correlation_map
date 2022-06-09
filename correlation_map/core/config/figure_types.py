"""Figure types configuration

Contains figure type enum class with all project available figure types.
"""
from enum import Enum
from typing import Optional


class FigureType(Enum):
    """Available figure types"""

    DEFAULT_IMAGE = "default image"
    SOURCE_IMAGE = "source image"
    DESTINATION_IMAGE = "destination image"
    CROPPED_IMAGE = "source cropped image"
    DETECTED_IMAGE = "destination detected image"
    ROTATED_IMAGE = "destination rotated image"
    FOUND_IMAGE = "destination found image"
    FOUND_AND_CROPPED = "destination found and cropped image"
    CORRELATION_MAP = "correlation map"

    @classmethod
    def get_by_name(cls, name: str) -> Optional['FigureType']:
        """Get figure type by name

        :param name: type of the figure
        :return: figure type enum model
        """
        for figure_type in FigureType:
            if name.lower() == figure_type.value:
                return figure_type
        return None
