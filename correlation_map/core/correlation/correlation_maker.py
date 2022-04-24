"""Module contains different correlation operations within a single class"""
import math

import numpy as np
from numpy import ndarray


class CorrelationMaker:
    """Provide different correlation methods"""

    __slots__ = []

    @classmethod
    def square_difference_correlation(cls, x_array: ndarray, y_array: ndarray) -> float:
        """Returns the square correlation coefficient for two matrices"""
        return float(np.sum(np.power(x_array - y_array, 2)))

    @classmethod
    def square_difference_normed_correlation(cls, x_array: ndarray, y_array: ndarray) -> float:
        """Returns the normed correlation coefficient for two matrices"""
        numerator = np.sum(np.power(x_array - y_array, 2))
        first_denominator = np.sum(np.power(x_array, 2))
        second_denominator = np.sum(np.power(y_array, 2))
        denominator = math.sqrt(first_denominator * second_denominator)
        return numerator / denominator if denominator != 0 else 1

    @classmethod
    def cross_correlation(cls, x_array: ndarray, y_array: ndarray) -> float:
        """Returns the cross correlation coefficient for two matrices"""
        return float(np.sum(x_array * y_array))

    @classmethod
    def cross_correlation_normed(cls, x_array: ndarray, y_array: ndarray) -> float:
        """Returns the normed correlation coefficient for two matrices"""
        numerator = np.sum(x_array * y_array)
        first_denominator = np.sum(np.power(x_array, 2))
        second_denominator = np.sum(np.power(y_array, 2))
        denominator = math.sqrt(first_denominator * second_denominator)
        return numerator / denominator if denominator != 0 else 1

    @classmethod
    def correlation_coefficient(cls, x_array: ndarray, y_array: ndarray) -> float:
        """Returns the correlation coefficient for two matrices"""
        x_average = np.sum(x_array) / np.size(x_array)
        y_average = np.sum(y_array) / np.size(y_array)
        return float(np.sum((x_array - x_average) * (y_array - y_average)))

    @classmethod
    def correlation_coefficient_normed(cls, x_array: ndarray, y_array: ndarray) -> float:
        """Returns the normed correlation coefficient for two matrices"""
        x_average = np.sum(x_array) / np.size(x_array)
        y_average = np.sum(y_array) / np.size(y_array)
        numerator = np.sum((x_array - x_average) * (y_array - y_average))
        first_denominator = np.sum(np.power(x_array - x_average, 2))
        second_denominator = np.sum(np.power(y_array - y_average, 2))
        denominator = math.sqrt(first_denominator * second_denominator)
        return numerator / denominator if denominator != 0 else 1
