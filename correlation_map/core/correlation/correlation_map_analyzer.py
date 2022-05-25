from dataclasses import dataclass

import cv2
import numpy as np

from correlation_map.core.config.figure_types import FigureType
from correlation_map.core.models.figures.correlation_map import CorrelationMap
from correlation_map.core.models.figures.figure_container import FigureContainer
from correlation_map.core.models.figures.image import ImageWrapper


@dataclass
class CorrelationMapAnalyzesSettings:
    """Correlation map analyzes settings

    Settings for analyzing and marking correlation map and their images

    Fields:
    search_limit: percent from 0% to 100% to determinate difference sensitivity
    """

    search_limit: int


class CorrelationMapAnalyzer:
    @classmethod
    def build_images_with_difference(cls, correlation_map_analyzes_settings: CorrelationMapAnalyzesSettings):
        correlation_map = FigureContainer.get(FigureType.CORRELATION_MAP)
        source_image = FigureContainer.get(FigureType.SOURCE_IMAGE)
        destination_image = FigureContainer.get(FigureType.DESTINATION_IMAGE)

        source_with_analyzes_image = cls._mark_correlation_map_difference(
            correlation_map_analyzes_settings, correlation_map, source_image)
        FigureContainer.add(source_with_analyzes_image)
        destination_with_analyzes_image = cls._mark_correlation_map_difference(
            correlation_map_analyzes_settings, correlation_map, destination_image)
        FigureContainer.add(destination_with_analyzes_image)

    @classmethod
    def _mark_correlation_map_difference(cls, correlation_map_analyzes_settings: CorrelationMapAnalyzesSettings,
                                         correlation_map: CorrelationMap,
                                         destination_image: ImageWrapper) -> ImageWrapper:
        matched_difference = np.ma.masked_where(
            0.8 > correlation_map.correlation_map,
            correlation_map.correlation_map
        )
