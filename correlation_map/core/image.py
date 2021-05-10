from typing import Tuple

import cv2
import numpy as np


class Image:
    def __init__(self, path: str):
        self.path = path
        self.image = self.__load_image()

    def __load_image(self):
        return cv2.imread(self.path)

    @property
    def shape(self) -> Tuple[int, int, int]:
        return self.image.shape

    def show(self):
        cv2.imshow("Test image", self.image)


class ImageBuilder:
    def transform_image_to_gray(self, image: Image) -> Image:
        """Returns the image matrix of which was converted on a gray scale of intensity"""
        gray_image = Image("1")
        gray_image.image = np.copy(image.image)
        for column_number, column in enumerate(gray_image.image):
            for row_number, pixel in enumerate(column):
                gray_image.image[column_number, row_number] = self.__make_gray_pixel(pixel)
        return gray_image

    def rotate_image(self, angle: float) -> Image:
        pass

    @staticmethod
    def __make_gray_pixel(pixel: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """
        Transform RGB pixel to red

        :param pixel: RGB pixel
        :return: Gray pixel
        """
        red, green, blue = pixel
        mean_intensity = round((int(red) + int(green) + int(blue)) / 3)
        return mean_intensity, mean_intensity, mean_intensity
