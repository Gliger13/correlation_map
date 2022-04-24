"""Abstract base class for all figures"""
from abc import ABCMeta, abstractmethod

from matplotlib.axes import Axes

from correlation_map.core.config.figure_types import FigureType


class BaseFigure(metaclass=ABCMeta):
    """Base figure for all images and maps"""

    @property
    @abstractmethod
    def figure_type(self) -> FigureType:
        """Abstract property to return figure type """

    @abstractmethod
    def show(self):
        """Show figure in matplotlib window with tools"""

    @abstractmethod
    def configure_figure_axes(self, axes: Axes) -> Axes:
        """
        Configure figure axes and return it

        :param axes: figure axes to configure
        :return: configured figure axes
        """

    @abstractmethod
    def save(self, path: str):
        """Save the figure in the specified directory path

        :param path: path to the directory to save
        """
