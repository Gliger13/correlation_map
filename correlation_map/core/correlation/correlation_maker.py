import math
from enum import Enum

import cv2
import numpy as np


class CorrelationTypes(Enum):
    TM_SQDIFF = "square_difference_correlation"
    TM_SQDIFF_NORMED = "square_difference_normed_correlation"
    TM_CCORR = "cross_correlation"
    TM_CCORR_NORMED = "cross_correlation_normed"
    TM_CCOEFF = "correlation_coefficient"
    TM_CCOEFF_NORMED = "correlation_coefficient_normed"


class CorrelationCV2Types(Enum):
    TM_SQDIFF = cv2.TM_SQDIFF
    TM_SQDIFF_NORMED = cv2.TM_SQDIFF_NORMED
    TM_CCORR = cv2.TM_CCORR
    TM_CCORR_NORMED = cv2.TM_CCORR_NORMED
    TM_CCOEFF = cv2.TM_CCOEFF
    TM_CCOEFF_NORMED = cv2.TM_CCOEFF_NORMED


class CorrelationMaker:
    @classmethod
    def square_difference_correlation(cls, inten_m1, inten_m2) -> float:
        numerator = float(np.sum(np.power(inten_m1 - inten_m2, 2)))
        return numerator

    @classmethod
    def square_difference_normed_correlation(cls, inten_m1, inten_m2) -> float:
        """Returns the normed correlation coefficient for two matrices"""
        numerator = np.sum(np.power(inten_m1 - inten_m2, 2))
        denominator1 = np.sum(np.power(inten_m1, 2))
        denominator2 = np.sum(np.power(inten_m2, 2))
        denominator = math.sqrt(denominator1 * denominator2)
        return numerator / denominator

    @classmethod
    def cross_correlation(cls, inten_m1, inten_m2) -> float:
        numerator = np.sum(inten_m1 * inten_m2)
        return float(numerator)

    @classmethod
    def cross_correlation_normed(cls, inten_m1, inten_m2) -> float:
        """Returns the normed correlation coefficient for two matrices"""
        numerator = np.sum(inten_m1 * inten_m2)
        denominator1 = np.sum(np.power(inten_m1, 2))
        denominator2 = np.sum(np.power(inten_m2, 2))
        denominator = math.sqrt(denominator1 * denominator2)
        return numerator / denominator

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
