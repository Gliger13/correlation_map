"""Contains all available image types and image wrapper model"""
import os
from enum import Enum
from typing import Optional, Tuple

import cv2
from filetype import guess
from matplotlib import pyplot as plt
from numpy import ndarray

from correlation_map.gui.tools.logger import app_logger


class ImageTypes(Enum):
    """Available image types"""

    DEFAULT_IMAGE = "default image"
    SOURCE_IMAGE = "source image"
    DESTINATION_IMAGE = "destination image"
    CROPPED_IMAGE = "source cropped image"
    DETECTED_IMAGE = "destination detected image"
    ROTATED_IMAGE = "destination rotated image"
    FOUND_IMAGE = "destination found image"
    FOUND_AND_CROPPED = "destination found and cropped image"
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


class ImageWrapper:
    """Image wrapper model"""

    def __init__(self, path: str = None, image_type: ImageTypes = None):
        """Checks the given image type and load image by the given path

        :param path: path to the image to load
        :param image_type: type of the image
        :raise TypeError: when provided incorrect image type
        """
        self.path = path
        self.image_type = image_type
        self._image_format = guess(self.path).extension if self.path else "png"
        self.image: Optional[ndarray] = cv2.cvtColor(cv2.imread(self.path), cv2.COLOR_BGR2RGB) if self.path else None

    def save(self, path: str):
        """Save the image in the specified directory path

        :param path: path to the directory to save
        """
        app_logger.debug("Saving image with type %s by path %s", self.image_type.value, path)
        if self.image is None:
            app_logger.warning("Can not save image with type %s, it's empty", self.image_type.value)
            return

        new_image_path = os.path.join(path, f"{self.image_type.value.replace(' ', '_')}.{self._image_format}")
        cv2.imwrite(new_image_path, self.image)
        app_logger.info("Image with type %s saved in path %s", self.image_type.value, path)

    @classmethod
    def create_image(cls, image: ndarray, image_type: Optional[ImageTypes] = None) -> 'ImageWrapper':
        """Create a new image by the given arrays

        :param image: arrays of the image to create
        :param image_type: type of the new image
        :return: created image wrapper with the given array and type
        """
        new_image = ImageWrapper(image_type=image_type)
        new_image.image = image
        return new_image

    @property
    def shape(self) -> Tuple[int, int, int]:
        """Return current images shapes

        :return: tuple of image shapes
        """
        if self.image is None:
            app_logger.warning("Can not get image shapes with type %s, it's empty", self.image_type.value)
            return 0, 0, 0
        return self.image.shape

    def show(self):
        """Show current image as matplotlib figure"""
        app_logger.debug("Showing image in the new window")
        if self.image is None:
            app_logger.warning("Can not show image with type %s, it's empty", self.image_type.value)
            return None
        plt.imshow(self.image)
        plt.title(self.image_type.value.capitalize())
        plt.show()
        return None
