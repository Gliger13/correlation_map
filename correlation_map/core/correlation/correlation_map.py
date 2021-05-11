import logging
import math

import numpy as np
from matplotlib import pyplot as plt

from core.correlation.correlation_maker import CorrelationMaker, CorrelationTypes
from core.images.image import Image, ImageTypes
from core.images.image_builder import ImageBuilder


class CorrelationMap:
    def __init__(self, source_image: Image, destination_image: Image, correlation_type: str, delim: int = 10):
        self.source_image = source_image
        self.destination_image = destination_image
        self.correlation_type = correlation_type
        self.delim = delim
        self.correlation_map = None

    @staticmethod
    def __make_equals(c1, c2):
        h1, w1 = c1.shape
        h2, w2 = c2.shape
        if h1 < h2:
            c2 = c2[:h1]
        else:
            c1 = c1[:h2]
        if w1 < w2:
            c2 = c2[:, :w1]
        else:
            c1 = c1[:, :w2]
        return c1, c2

    def build_correlation_map(self):
        gray_source_matrix = ImageBuilder.transform_image_to_gray(self.source_image).image
        gray_destination_matrix = ImageBuilder.transform_image_to_gray(self.destination_image).image

        h1, w1, _ = gray_source_matrix.shape
        h2, w2, _ = gray_destination_matrix.shape

        if h1 * w1 < h2 * w2:
            self.correlation_map = np.zeros((math.ceil(h1 / self.delim), math.ceil(w1 / self.delim)))
        else:
            self.correlation_map = np.zeros((math.ceil(h2 / self.delim), math.ceil(w2 / self.delim)))

        cells_1 = []
        for i, row_i in enumerate(range(0, len(gray_source_matrix), self.delim)):
            for j, column_i in enumerate(range(0, len(gray_source_matrix[i]), self.delim)):
                cell = gray_source_matrix[row_i:row_i + self.delim, column_i:column_i + self.delim]
                cells_1.append(cell)

        cells_2 = []
        for i, row_i in enumerate(range(0, len(gray_destination_matrix), self.delim)):
            for j, column_i in enumerate(range(0, len(gray_destination_matrix[i]), self.delim)):
                cell = gray_destination_matrix[row_i:row_i + self.delim, column_i:column_i + self.delim]
                cells_2.append(cell)

        logging.debug('Start correlation')
        cells_left = min(len(cells_1), len(cells_2))
        current_cell = 1
        for i, row in enumerate(self.correlation_map):
            for j, _ in enumerate(row):
                logging.debug(f'Calc {current_cell}/{cells_left}')
                cell1 = cells_1.pop(0)
                cell2 = cells_2.pop(0)
                if cell1.shape != cell2.shape:
                    cell1, cell2 = self.__make_equals(cell1, cell2)

                correlation_function_name = CorrelationTypes[self.correlation_type].value
                cell_correlation = CorrelationMaker().__getattribute__(correlation_function_name)(cell1, cell2)
                self.correlation_map[i, j] = cell_correlation
                current_cell += 1

        return self

    def view_correlation_map(self):
        x_array = []
        y_array = []
        z_array = []
        for i, row in enumerate(self.correlation_map):
            for j, _ in enumerate(row):
                x_array.append(i)
                y_array.append(j)
                z_array.append(self.correlation_map[i, j])
        ax = plt.axes(projection='3d')
        ax.plot_trisurf(x_array, y_array, z_array, linewidth=0.1, antialiased=True, cmap='magma')
        ax.set_title('Correlation map')
        plt.show()
        return x_array, y_array, z_array
