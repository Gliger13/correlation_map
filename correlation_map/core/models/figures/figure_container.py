"""Container model to store all generated figures

Contains singleton figure container that's responsible for storing and giving
latest generated or loaded figures by figure types.
"""
from typing import Generator, Optional

from correlation_map.core.config.figure_types import FigureType
from correlation_map.core.models.figures.base_figure import BaseFigure
from correlation_map.core.tools.common import MetaSingleton
from correlation_map.gui.tools.logger import app_logger


class FigureContainer(metaclass=MetaSingleton):
    """Container to store and give latest generated or loaded figures by type"""

    __figures: dict[FigureType, BaseFigure] = {}

    @classmethod
    def add(cls, figure: BaseFigure):
        """Add the given figure to the figure container"""
        cls.__figures[figure.figure_type] = figure
        app_logger.debug("New figure with type `%s` registered in the figure container", figure.figure_type.value)

    @classmethod
    def get(cls, figure_type: FigureType) -> Optional[BaseFigure]:
        """Get figure from the container by given figure type

        :param figure_type: type of the figure to get
        :return: figure from the container with the given type if it exists
        """
        if figure := cls.__figures.get(figure_type):
            return figure
        app_logger.warning("No figure with type % received from the container. Doesn't exist", figure_type.value)
        return None

    @classmethod
    def get_all_user_images(cls) -> Generator[BaseFigure, None, None]:
        """Get generator that returns all figures except default"""
        for figure in cls.__figures.values():
            if figure.figure_type != FigureType.DEFAULT_IMAGE:
                yield figure

    @classmethod
    def is_contains_user_images(cls) -> bool:
        """Returns True if there is any user figure in the container else False"""
        return any(figure for figure in cls.__figures.values() if figure.figure_type != FigureType.DEFAULT_IMAGE)

    @classmethod
    def is_contain_specific_image(cls, figure_type: FigureType) -> bool:
        """Returns True if the figure container contains the figure with the given type else False"""
        return figure_type in cls.__figures

    @classmethod
    def get_all_figure_types(cls) -> list[str]:
        """Get all figure types in the container

        :return: all types of the figures in the container
        """
        return [figure.figure_type.value for figure in cls.__figures.values()]
