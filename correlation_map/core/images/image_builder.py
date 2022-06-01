"""Module contains image builder class for transforming images"""
import cv2
import numpy as np
from numpy import ndarray

from correlation_map.core.models.figures.image import FigureType, ImageWrapper
from correlation_map.core.models.image_selected_region import ImageSelectedRegion


class ImageBuilder:
    """Contains actions and transformations for images"""

    @classmethod
    def transform_image_to_gray(cls, image: ImageWrapper) -> ImageWrapper:
        """Returns the image matrix of which was converted on a gray scale of intensity

        :param image: image to make gray
        :return: image in gray scale
        """
        gray_image = np.zeros(image.shape[:2])
        for column_number, column in enumerate(image.image):
            for row_number, pixel in enumerate(column):
                gray_image[column_number, row_number] = cls.__make_gray_pixel(pixel)
        return ImageWrapper.create_image(gray_image)

    @classmethod
    def rotate_image(cls, image: ImageWrapper, angle: float) -> ImageWrapper:
        """Rotate the image by the given angle relative to the center of image

        :param image: image to rotate
        :param angle: rotation angle
        :return: rotated image
        """
        height, weight, _ = image.image.shape
        image_center = height / 2, weight / 2
        matrix = cv2.getRotationMatrix2D(image_center, angle, 1.0)
        rotated_image = cv2.warpAffine(image.image, matrix, (weight, height))
        return ImageWrapper.create_image(rotated_image, FigureType.ROTATED_IMAGE)

    @classmethod
    def crop_image(cls, image: ImageWrapper, image_selection: ImageSelectedRegion) -> ImageWrapper:
        """Crop image according to the given top left and bottom right region coordinates

        :param image: image to crop
        :param image_selection: rectangle coordinates to crop
        :return: cropped image
        """
        return ImageWrapper.create_image(cls._crop_image(image.image, image_selection), FigureType.CROPPED_IMAGE)

    @classmethod
    def mark_found_image(cls, image: ImageWrapper, image_selection: ImageSelectedRegion) -> ImageWrapper:
        """Mark the given region in the given image

        :param image: image to draw in it
        :param image_selection: image area coordinates to draw along the path
        :return: image with drawn area
        """
        image_with_rectangle = ImageWrapper.create_image(image.image.copy(), FigureType.FOUND_IMAGE)
        cv2.rectangle(
            image_with_rectangle.image, image_selection.top_left_point, image_selection.bottom_right_point, 255, 2)
        return image_with_rectangle

    @classmethod
    def crop_found_image(cls, image: ImageWrapper, image_selection: ImageSelectedRegion) -> ImageWrapper:
        """Crop image according to the given image selection

        :param image: image to crop
        :param image_selection: rectangle coordinates to crop
        :return: cropped found image
        """
        return ImageWrapper.create_image(cls._crop_image(image.image, image_selection), FigureType.FOUND_AND_CROPPED)

    @classmethod
    def _crop_image(cls, image: ndarray, image_selection: ImageSelectedRegion) -> ndarray:
        """Crop image according to the given top left and bottom right region coordinates

        :param image: image numpy arrays
        :param image_selection: rectangle coordinates to crop
        :return: cut image numpy arrays
        """
        return image[
               min(image_selection.y_1, image_selection.y_2):max(image_selection.y_1, image_selection.y_2),
               min(image_selection.x_1, image_selection.x_2):max(image_selection.x_1, image_selection.x_2)]

    @staticmethod
    def __make_gray_pixel(pixel: tuple[int, int, int]) -> int:
        """Transform RGB pixel to gray

        :param pixel: RGB pixel attributes
        :return: gray pixel attributes
        """
        return round(sum(pixel) / len(pixel))
