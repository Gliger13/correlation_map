"""Contains all available image types and image wrapper model"""
from ctypes import Array
from enum import Enum
from typing import Optional, Tuple

import cv2
from matplotlib.image import imread


class ImageTypes(Enum):
    """Available image types"""

    DEFAULT_IMAGE = "default image"
    SOURCE_IMAGE = "source image"
    DESTINATION_IMAGE = "destination image"
    SCALED_IMAGE = "scaled image"
    DETECTED_IMAGE = "detected image"
    ROTATED_IMAGE = "rotated image"
    FOUND_IMAGE = "found image"
    FOUND_AND_CROPPED = "found and cropped image"
    CORRELATION_MAP = "correlation map"

    @classmethod
    def get_by_name(cls, name: str) -> Optional['ImageTypes']:
        """Get image type by name

        :param name: type of the image
        :return: image type enum model
        """
        for image_type in ImageTypes:
            if name.lower() == image_type.value:
                return image_type
        return None


class Image:
    """Image wrapper model"""

    def __init__(self, path: str = None, image_type: ImageTypes = None):
        """Checks the given image type and load image by the given path

        :param path: path to the image to load
        :param image_type: type of the image
        :raise TypeError: when provided incorrect image type
        """
        self.path = path
        self.image_type = image_type
        if self.image_type not in ImageTypes:
            raise TypeError(f"Image type `{self.image_type}` not supported")
        self.image = imread(self.path)

    def save(self, path: str):
        """Save image by the given path"""
        self.image.save(path)

    @classmethod
    def create_image(cls, image: Array, image_type: ImageTypes = None) -> 'Image':
        """Create new image by the given arrays

        :param image: arrays of the image to create
        :param image_type: type of the new image
        :return: created image wrapper with the given array and type
        """
        new_image = Image(image_type=image_type)
        new_image.image = image
        return new_image

    @property
    def shape(self) -> Tuple[int, int, int]:
        return self.image.shape

    def show(self):
        cv2.imshow("Test image", self.image)
