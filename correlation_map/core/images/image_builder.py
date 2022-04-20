"""Module contains image builder class for transforming images"""
import cv2
import numpy as np

from correlation_map.core.images.image import ImageTypes, ImageWrapper
from correlation_map.core.images.images_describer import ImageSelection


class ImageBuilder:
    """Contains actions and transformations for images"""

    @classmethod
    def transform_image_to_gray(cls, image: ImageWrapper) -> ImageWrapper:
        """Returns the image matrix of which was converted on a gray scale of intensity

        :param image: image to make gray
        :return: image in gray scale
        """
        gray_image = np.copy(image.image)
        for column_number, column in enumerate(gray_image):
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
        return ImageWrapper.create_image(rotated_image, ImageTypes.ROTATED_IMAGE)

    @classmethod
    def crop_image(cls, image: ImageWrapper, top_left: tuple[int, int], bottom_right: tuple[int, int]) -> ImageWrapper:
        """Crop image according to the given top left and bottom right region coordinates

        :param image: image to crop
        :param top_left: tuple of x and y coordinates of the top left point in the image area to have
        :param bottom_right: tuple of x and y coordinates of the bottom right point in the image area to have
        :return: cropped image
        """
        x1, y1 = top_left
        x2, y2 = bottom_right
        return ImageWrapper.create_image(
            image.image[min(y1, y2):max(y1, y2), min(x1, x2):max(x1, x2)], ImageTypes.CROPPED_IMAGE)

    @classmethod
    def mark_found_image(cls, image: ImageWrapper, image_selection: ImageSelection) -> ImageWrapper:
        """Mark the given region in the given image

        :param image: image to draw in it
        :param image_selection: image area coordinates to draw along the path
        :return: image with drawn area
        """
        image_with_rectangle = ImageWrapper.create_image(image.image.copy(), ImageTypes.FOUND_IMAGE)
        cv2.rectangle(
            image_with_rectangle.image, image_selection.top_left_point, image_selection.bottom_right_point, 255, 2)
        return image_with_rectangle

    @classmethod
    def crop_found_image(cls, source_image: ImageWrapper, image_selection: ImageSelection) -> ImageWrapper:
        """TODO: Delete"""
        cropped_image = source_image.image[
                        min(image_selection.y1, image_selection.y2):max(image_selection.y1, image_selection.y2),
                        min(image_selection.x1, image_selection.x2):max(image_selection.x1, image_selection.x2)]
        return ImageWrapper.create_image(cropped_image, ImageTypes.FOUND_AND_CROPPED)

    @staticmethod
    def __make_gray_pixel(pixel: tuple[int, int, int]) -> tuple[int, int, int]:
        """Transform RGB pixel to gray

        :param pixel: RGB pixel attribues
        :return: gray pixel attributes
        """
        red, green, blue = pixel
        mean_intensity = round((int(red) + int(green) + int(blue)) / 3)
        return mean_intensity, mean_intensity, mean_intensity
