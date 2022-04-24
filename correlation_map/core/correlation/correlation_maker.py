"""Module contains methods and classes to make different correlation operators"""
import math
from enum import Enum

import cv2
import numpy as np


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


class CorrelationMaker:
    """Class contains different correlation operations"""

    @classmethod
    def square_difference_correlation(cls, inten_m1, inten_m2) -> float:
        """Returns the square correlation coefficient for two matrices"""
        numerator = float(np.sum(np.power(inten_m1 - inten_m2, 2)))
        return numerator

    @classmethod
    def square_difference_normed_correlation(cls, inten_m1, inten_m2) -> float:
        """Returns the normed correlation coefficient for two matrices"""
        numerator = np.sum(np.power(inten_m1 - inten_m2, 2))
        denominator1 = np.sum(np.power(inten_m1, 2))
        denominator2 = np.sum(np.power(inten_m2, 2))
        denominator = math.sqrt(denominator1 * denominator2)
        return numerator / denominator if denominator != 0 else 1

    @classmethod
    def cross_correlation(cls, inten_m1, inten_m2) -> float:
        """Returns the cross correlation coefficient for two matrices"""
        numerator = np.sum(inten_m1 * inten_m2)
        return float(numerator)

    @classmethod
    def cross_correlation_normed(cls, inten_m1, inten_m2) -> float:
        """Returns the normed correlation coefficient for two matrices"""
        numerator = np.sum(inten_m1 * inten_m2)
        denominator1 = np.sum(np.power(inten_m1, 2))
        denominator2 = np.sum(np.power(inten_m2, 2))
        denominator = math.sqrt(denominator1 * denominator2)
        return numerator / denominator if denominator != 0 else 1

    @classmethod
    def correlation_coefficient(cls, inten_m1, inten_m2) -> float:
        """Returns the correlation coefficient for two matrices"""
        avg_intensity1 = np.sum(inten_m1) / np.size(inten_m1)
        avg_intensity2 = np.sum(inten_m2) / np.size(inten_m2)
        numerator = float(np.sum((inten_m1 - avg_intensity1) * (inten_m2 - avg_intensity2)))
        return numerator

    @classmethod
    def correlation_coefficient_normed(cls, inten_m1, inten_m2) -> float:
        """Returns the normed correlation coefficient for two matrices"""
        avg_intensity1 = np.sum(inten_m1) / np.size(inten_m1)
        avg_intensity2 = np.sum(inten_m2) / np.size(inten_m2)
        numerator = np.sum((inten_m1 - avg_intensity1) * (inten_m2 - avg_intensity2))
        denominator1 = np.sum(np.power(inten_m1 - avg_intensity1, 2))
        denominator2 = np.sum(np.power(inten_m2 - avg_intensity2, 2))
        denominator = math.sqrt(denominator1 * denominator2)
        return numerator / denominator if denominator != 0 else 1
