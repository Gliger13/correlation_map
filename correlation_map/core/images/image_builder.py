from typing import Tuple

import cv2
import numpy as np

from correlation_map.core.images.image import ImageTypes, ImageWrapper
from correlation_map.core.images.images_describer import ImagesDescriber, ImageSelection


class ImageBuilder:
    @classmethod
    def transform_image_to_gray(cls, image: ImageWrapper) -> ImageWrapper:
        """Returns the image matrix of which was converted on a gray scale of intensity

        :param image: Source image
        :return: Gray image
        """
        gray_image = np.copy(image.image)
        for column_number, column in enumerate(gray_image):
            for row_number, pixel in enumerate(column):
                gray_image[column_number, row_number] = cls.__make_gray_pixel(pixel)
        return ImageWrapper.create_image(gray_image)

    @classmethod
    def rotate_image(cls, image: ImageWrapper, angle: float) -> ImageWrapper:
        """
        Rotate the image by theta degrees relative to the center of image

        :param image: Source image
        :param angle: Angle of rotation
        :return: Rotated image
        """
        height, weight, _ = image.image.shape
        image_center = height / 2, weight / 2
        matrix = cv2.getRotationMatrix2D(image_center, angle, 1.0)
        rotated_image = cv2.warpAffine(image.image, matrix, (weight, height))
        return ImageWrapper.create_image(rotated_image, ImageTypes.ROTATED_IMAGE)

    @classmethod
    def scale_image(cls, image: ImageWrapper, top_left: Tuple[int, int], bottom_right: Tuple[int, int]) -> ImageWrapper:
        x1, y1 = top_left
        x2, y2 = bottom_right
        return ImageWrapper.create_image(image.image[y1:y2, x1:x2], ImageTypes.SCALED_IMAGE)

    @classmethod
    def _mark_found_image(cls, source_image: ImageWrapper, image_selection: ImageSelection) -> ImageWrapper:
        image_with_rectangle = ImageWrapper.create_image(source_image.image.copy(), ImageTypes.FOUND_IMAGE)
        cv2.rectangle(image_with_rectangle.image,
                      image_selection.top_left_point, image_selection.bottom_right_point, 255, 2)
        return image_with_rectangle

    @classmethod
    def _crop_found_image(cls, source_image: ImageWrapper, image_selection: ImageSelection) -> ImageWrapper:
        cropped_image = source_image.image[image_selection.y2:image_selection.y1,
                                           image_selection.x2:image_selection.x1]
        return ImageWrapper.create_image(cropped_image, ImageTypes.FOUND_AND_CROPPED)

    @classmethod
    def find_and_cut(cls, source_image: ImageWrapper, destination_image: ImageWrapper,
                     type_of_correlation: str) -> Tuple[ImageWrapper, ImageWrapper]:
        image_selection = ImagesDescriber.find_image_points(source_image, destination_image, type_of_correlation)

        marked_image = cls._mark_found_image(source_image, image_selection)
        cropped_image = cls._crop_found_image(source_image, image_selection)
        return marked_image, cropped_image

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
