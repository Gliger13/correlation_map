"""Contains all available image types and image wrapper model"""
import os
from typing import Optional, Tuple

import cv2
from filetype import guess
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from numpy import ndarray

from correlation_map.core.config.figure_types import FigureType
from correlation_map.core.models.figures.base_figure import BaseFigure
from correlation_map.gui.tools.logger import app_logger


class ImageWrapper(BaseFigure):
    """Figure implementation for the image"""

    def __init__(self, path: str = None, image_type: FigureType = None):
        """Checks the given image type and load image by the given path

        :param path: path to the image to load
        :param image_type: type of the image
        :raise TypeError: when provided incorrect image type
        """
        self.path = path
        self.image_type = image_type
        self._image_format = guess(self.path).extension if self.path else "png"
        self.image: Optional[ndarray] = cv2.cvtColor(cv2.imread(self.path), cv2.COLOR_BGR2RGB) if self.path else None

    @property
    def figure_type(self) -> FigureType:
        """Return image type"""
        return self.image_type

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

    def configure_figure_axes(self, axes: Axes) -> Axes:
        """Configure figure axes and return it

        Configuration:
        - Add current image data arrays to the given axes
        - Set plot title
        """
        axes.imshow(self.image)
        axes.set_title(self.image_type.value.capitalize())
        return axes

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
    def create_image(cls, image: ndarray, image_type: Optional[FigureType] = None) -> 'ImageWrapper':
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
