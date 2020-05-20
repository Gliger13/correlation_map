import logging
import math

import cv2
import numpy as np
from matplotlib import pyplot as plt

import img_process

logging.basicConfig(level=logging.DEBUG)

TYPES_OF_CORRELATION = {
    "TM_SQDIFF": cv2.TM_SQDIFF, "TM_SQDIFF_NORMED": cv2.TM_SQDIFF_NORMED,
    "TM_CCORR": cv2.TM_CCORR, "TM_CCORR_NORMED": cv2.TM_CCORR_NORMED,
    "TM_CCOEFF": cv2.TM_CCOEFF, "TM_CCOEFF_NORMED": cv2.TM_CCOEFF_NORMED
}


def sqdiff(inten_m1, inten_m2) -> float:
    numerator = float(np.sum(np.power(inten_m1 - inten_m2, 2)))
    return numerator


def sqdiff_normed(inten_m1, inten_m2) -> float:
    """Returns the normed correlation coefficient for two matrices"""
    numerator = np.sum(np.power(inten_m1 - inten_m2, 2))
    denominator1 = np.sum(np.power(inten_m1, 2))
    denominator2 = np.sum(np.power(inten_m2, 2))
    denominator = math.sqrt(denominator1 * denominator2)
    return numerator / denominator


def ccorr(inten_m1, inten_m2) -> float:
    numerator = np.sum(inten_m1 * inten_m2)
    return float(numerator)


def ccorr_normed(inten_m1, inten_m2) -> float:
    """Returns the normed correlation coefficient for two matrices"""
    numerator = np.sum(inten_m1 * inten_m2)
    denominator1 = np.sum(np.power(inten_m1, 2))
    denominator2 = np.sum(np.power(inten_m2, 2))
    denominator = math.sqrt(denominator1 * denominator2)
    return numerator / denominator


def ccoeff(inten_m1, inten_m2) -> float:
    """Returns the correlation coefficient for two matrices"""
    avg_intensity1 = np.sum(inten_m1) / np.size(inten_m1)
    avg_intensity2 = np.sum(inten_m2) / np.size(inten_m2)
    numerator = float(np.sum((inten_m1 - avg_intensity1) * (inten_m2 - avg_intensity2)))
    return numerator


def ccoeff_normed(inten_m1, inten_m2) -> float:
    """Returns the normed correlation coefficient for two matrices"""
    avg_intensity1 = np.sum(inten_m1) / np.size(inten_m1)
    avg_intensity2 = np.sum(inten_m2) / np.size(inten_m2)
    numerator = np.sum((inten_m1 - avg_intensity1) * (inten_m2 - avg_intensity2))
    denominator1 = np.sum(np.power(inten_m1 - avg_intensity1, 2))
    denominator2 = np.sum(np.power(inten_m2 - avg_intensity2, 2))
    denominator = math.sqrt(denominator1 * denominator2)
    return numerator / denominator if denominator != 0 else 1


FUNCS_OF_CORRELATION = {
    "TM_SQDIFF": sqdiff, "TM_SQDIFF_NORMED": sqdiff_normed,
    "TM_CCORR": ccorr, "TM_CCORR_NORMED": ccorr_normed,
    "TM_CCOEFF": ccoeff, "TM_CCOEFF_NORMED": ccoeff_normed
}


def corr_map(img1, img2, delim=10, correlation_name="TM_CCOEFF_NORMED"):
    def make_equals(c1, c2):
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

    matr1 = img_process.img_to_matrix(img1)
    matr2 = img_process.img_to_matrix(img2)
    logging.debug('Translated image to matrix')

    h1, w1 = matr1.shape
    h2, w2 = matr2.shape
    if h1 * w1 < h2 * w2:
        correlation_map = np.zeros((math.ceil(h1 / delim), math.ceil(w1 / delim)))
    else:
        correlation_map = np.zeros((math.ceil(h2 / delim), math.ceil(w2 / delim)))
    cells_1 = []
    for i, row_i in enumerate(range(0, len(matr1), delim)):
        for j, column_i in enumerate(range(0, len(matr1[i]), delim)):
            cell = matr1[row_i:row_i + delim, column_i:column_i + delim]
            cells_1.append(cell)
    cells_2 = []
    for i, row_i in enumerate(range(0, len(matr2), delim)):
        for j, column_i in enumerate(range(0, len(matr2[i]), delim)):
            cell = matr2[row_i:row_i + delim, column_i:column_i + delim]
            cells_2.append(cell)
    logging.debug('Divided matrix for pieces')

    logging.debug('Start correlation')
    cells_left = min(len(cells_1), len(cells_2))
    current_cell = 1
    for i, row in enumerate(correlation_map):
        for j, _ in enumerate(row):
            logging.debug(f'Calc {current_cell}/{cells_left}')
            cell1 = cells_1.pop(0)
            cell2 = cells_2.pop(0)
            if cell1.shape != cell2.shape:
                cell1, cell2 = make_equals(cell1, cell2)
            cell_correlation = FUNCS_OF_CORRELATION[correlation_name](cell1, cell2)
            correlation_map[i, j] = cell_correlation
            current_cell += 1
    return correlation_map


def view_map(c_map):
    x_array = []
    y_array = []
    z_array = []
    for i, row in enumerate(c_map):
        for j, _ in enumerate(row):
            x_array.append(i)
            y_array.append(j)
            z_array.append(c_map[i, j])
    ax = plt.axes(projection='3d')
    ax.plot_trisurf(x_array, y_array, z_array, linewidth=0.1, antialiased=True, cmap='magma')
    ax.set_title('Correlation map')
    plt.show()
    return x_array, y_array, z_array


def find_and_cut(source_img, finding_img, type_of_correlation):
    res = cv2.matchTemplate(source_img, finding_img, TYPES_OF_CORRELATION[type_of_correlation])
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    h, w = finding_img.shape[:2]
    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if TYPES_OF_CORRELATION[type_of_correlation] in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    marked_region = source_img.copy()
    cv2.rectangle(marked_region, top_left, bottom_right, 255, 2)
    source_img = source_img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    return marked_region, source_img
