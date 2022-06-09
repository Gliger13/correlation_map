"""Contains correlation map model"""
import logging
from collections import deque
from typing import Optional

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from numpy import ndarray

from correlation_map.core.config.correlation import CorrelationTypes
from correlation_map.core.config.figure_types import FigureType
from correlation_map.core.correlation.correlation_maker import CorrelationMaker
from correlation_map.core.images.image_builder import ImageBuilder
from correlation_map.core.models.figures.base_figure import BaseFigure
from correlation_map.core.models.figures.image import ImageWrapper
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

    def get_correlation_map_shapes(self, source_image_matrix: ndarray, destination_image: ndarray) -> tuple[int, int]:
        """Get correlation map shapes from the given image matrices

        :param source_image_matrix: source grayscale image matrix
        :param destination_image: destination grayscale image matrix
        :return: height and weight of the correlation map
        """
        height_1, weight_1 = source_image_matrix.shape
        height_2, weight_2 = destination_image.shape

        if height_1 * weight_1 < height_2 * weight_2:
            height, weight = height_1, weight_1
        else:
            height, weight = height_2, weight_2
        return height - round(height % self.pieces_amount), weight - round(weight % self.pieces_amount)

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
        height, weight = self.get_correlation_map_shapes(gray_source_matrix, gray_destination_matrix)
        self.correlation_map = np.zeros((height, weight))
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

        correlation_vector_deque: deque = deque()
        for current_cell_number, (source_cell, destination_cell) in enumerate(zip(source_cells, destination_cells)):
            app_logger.debug("Calculated %s/%s cells", current_cell_number, cells_to_process)
            cell_correlation = correlation_method(source_cell[0], destination_cell[0])
            correlation_vector_deque.append(cell_correlation)

        for i, row in enumerate(range(0, len(self.correlation_map), self.pieces_amount)):
            for _, column in enumerate(range(0, len(self.correlation_map[i]), self.pieces_amount)):
                correlation_part = np.full((self.pieces_amount, self.pieces_amount), correlation_vector_deque.popleft())
                map_part = self.correlation_map[row:row + self.pieces_amount, column:column + self.pieces_amount]
                self.correlation_map[row:row + map_part.shape[0], column:column + map_part.shape[1]] = correlation_part
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
