"""Contains correlation map model"""
import logging
import math
from collections import deque
from typing import Optional

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from numpy import ndarray

from correlation_map.core.config.correlation import CorrelationTypes
from correlation_map.core.config.figure_types import FigureType
from correlation_map.core.correlation.correlation_maker import CorrelationMaker
from correlation_map.core.models.figures.base_figure import BaseFigure
from correlation_map.core.models.figures.image import ImageWrapper
from correlation_map.core.images.image_builder import ImageBuilder
from correlation_map.gui.tools.logger import app_logger


class CorrelationMap(BaseFigure):
    """Correlation map figure model

    3d figure which shows correlation between source and destination image
    """

    def __init__(self, source_image: ImageWrapper, destination_image: ImageWrapper,
                 correlation_type: CorrelationTypes, pieces_amount: int = 10):
        self.source_image = source_image
        self.destination_image = destination_image
        self.correlation_type = correlation_type

        self.pieces_amount = pieces_amount
        self.correlation_map: Optional[ndarray] = None

    @property
    def figure_type(self) -> FigureType:
        """Return correlation map figure type"""
        return FigureType.CORRELATION_MAP

    def _get_cells_from_image_matrix(self, matrix: ndarray) -> deque[ndarray]:
        """Divide the given matrix by cells with the pieces amount shapes

        :param matrix: image matrix to divide
        :return: list of image matrix cells with the current pieces amount shapes
        """
        cells: deque[ndarray] = deque()
        for i, row_i in enumerate(range(0, len(matrix), self.pieces_amount)):
            for _, column_i in enumerate(range(0, len(matrix[i]), self.pieces_amount)):
                cells.append(matrix[row_i:row_i + self.pieces_amount, column_i:column_i + self.pieces_amount])
        return cells

    def _fill_correlation_map_with_zeroes(self, source_image_matrix: ndarray, destination_image: ndarray):
        """Fill correlation map with zeroes with the shapes of the given images

        :param source_image_matrix: source grayscale image matrix
        :param destination_image: destination grayscale image matrix
        """
        height_1, weight_1, _ = source_image_matrix.shape
        height_2, weight_2, _ = destination_image.shape

        if height_1 * weight_1 < height_2 * weight_2:
            self.correlation_map = np.zeros((
                math.ceil(height_1 / self.pieces_amount), math.ceil(weight_1 / self.pieces_amount)))
        else:
            self.correlation_map = np.zeros((
                math.ceil(height_2 / self.pieces_amount), math.ceil(weight_2 / self.pieces_amount)))

    def build_correlation_map(self) -> "CorrelationMap":
        """Calculate correlation map

        Transform source and destination image in grayscale. Slides through
        destination image, compares the overlapped pieces of the specific size
        from source image using the specified correlation type. Save calculated
        results as x_array, y_array, z_array in the current map.

        :return: calculated correlation map
        """
        app_logger.debug("Starting correlation map calculations")
        app_logger.debug("Transforming current source image to grayscale")
        gray_source_matrix = ImageBuilder.transform_image_to_gray(self.source_image).image
        app_logger.debug("Transforming current destination image to grayscale")
        gray_destination_matrix = ImageBuilder.transform_image_to_gray(self.destination_image).image
        app_logger.debug("Filling correlation map with zeroes using source and destination images shapes")
        self._fill_correlation_map_with_zeroes(gray_source_matrix, gray_destination_matrix)
        app_logger.debug("Dividing source image to cells with the %s height and %s weight",
                         self.pieces_amount, self.pieces_amount)
        source_cells = self._get_cells_from_image_matrix(gray_source_matrix)
        app_logger.debug("Dividing destination image to cells with the %s height and %s weight",
                         self.pieces_amount, self.pieces_amount)
        destination_cells = self._get_cells_from_image_matrix(gray_destination_matrix)

        cells_to_process = min(len(source_cells), len(destination_cells))
        app_logger.debug("Calculating correlations between source and destination cells. To calculate correlation for "
                         "%s cells", cells_to_process)
        correlation_method = CorrelationMaker().__getattribute__(self.correlation_type.correlation_type)
        for i, row in enumerate(self.correlation_map):
            for j, _ in enumerate(row):
                app_logger.debug("Calculated %s/%s cells", cells_to_process - len(source_cells), cells_to_process)
                source_cell = source_cells.popleft()
                destination_cell = destination_cells.popleft()
                if source_cell.shape != destination_cell.shape:
                    source_cell, destination_cell = self.__make_equals(source_cell, destination_cell)
                cell_correlation = correlation_method(source_cell, destination_cell)
                self.correlation_map[i, j] = cell_correlation
        return self

    def configure_figure_axes(self, axes: Axes) -> Axes:
        """Configure correlation map axes

        Configuration:
        - Add current correlation data arrays to the given axes
        - Set plot surface configuration
        - Add plot title

        :param axes: correlation map axes
        :return: configured correlation map axes
        """
        x_array, y_array, z_array, = self._get_correlation_map_arrays()
        axes.plot_trisurf(x_array, y_array, z_array, linewidth=0.1, antialiased=True, cmap="magma")
        axes.set_title("Correlation map")
        return axes

    def show(self):
        """View current correlation map as 3d matplotlib window"""
        app_logger.debug("Showing correlation map in the new window")
        if self.correlation_map is None:
            app_logger.warning("Can not show correlation map, it's not created")
            return None

        axes = plt.axes(projection="3d")
        self.configure_figure_axes(axes)
        plt.show()
        return None

    def save(self, path: str):
        """Save correlation map in the specified directory path

        :param path: path to the directory to save
        """
        logging.warning("Cannot save correlation map. Not implemented")

    def _get_correlation_map_arrays(self) -> tuple[list[float], list[float], list[float]]:
        """Return current correlation map arrays

        :return: tuple of x, y, z arrays
        """
        x_array, y_array, z_array = [], [], []
        for i, row in enumerate(self.correlation_map):
            for j, _ in enumerate(row):
                x_array.append(i)
                y_array.append(j)
                z_array.append(self.correlation_map[i, j])
        return x_array, y_array, z_array

    @staticmethod
    def __make_equals(cell_1: ndarray, cell_2: ndarray) -> tuple[ndarray, ndarray]:
        """Make numpy array cells have the same shapes

        Make given array cells have the same shapes by cutting and making them
        according to minimum shapes.

        :param cell_1: first numpy array cell to make the same shape as second
        :param cell_2: second numpy array cell to make the same shape as first
        :return: tuple of the first and second given numpy arrays with the same shapes
        """
        height_1, weight_1, *_ = cell_1.shape
        height_2, weight_2, *_ = cell_2.shape
        if height_1 < height_2:
            cell_2 = cell_2[:height_1]
        else:
            cell_1 = cell_1[:height_2]
        if weight_1 < weight_2:
            cell_2 = cell_2[:, :weight_1]
        else:
            cell_2 = cell_1[:, :weight_2]
        return cell_1, cell_2
