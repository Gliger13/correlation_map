"""Module contains image container singleton to store all images"""
import logging
from typing import Dict, Optional

from correlation_map.core.images.image import Image, ImageTypes
from correlation_map.core.tools.common import MetaSingleton
from correlation_map.gui.tools.logger import app_logger


class ImageContainer(metaclass=MetaSingleton):
    """Singleton container to store all images"""

    __images: Dict[ImageTypes, Image] = {}

    @classmethod
    def add(cls, image: Image):
        """Add the given image to images container"""
        cls.__images[image.image_type] = image
        app_logger.debug("New image with type `%s` registered in the image container", image.image_type.value)

    @classmethod
    def get(cls, image_type: ImageTypes) -> Optional[Image]:
        """Get image from container by given image type

        :param image_type: type of image to get
        :return: mage from container with given type if exists
        """
        if image := cls.__images.get(image_type):
            return image
        logging.warning("No image with type % received from container. Does not exist", image_type.value)
        return None

    @classmethod
    def get_loaded_image_types(cls) -> list[str]:
        """Get all image types in the container

        :return: all types of images from the container
        """
        return [image.image_type.value for image in cls.__images.values()]
