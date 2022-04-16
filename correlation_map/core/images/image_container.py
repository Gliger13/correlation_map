"""Module contains image container singleton to store all images"""
import logging
from typing import Dict, Generator, Optional

from correlation_map.core.images.image import ImageTypes, ImageWrapper
from correlation_map.core.tools.common import MetaSingleton
from correlation_map.gui.tools.logger import app_logger


class ImageContainer(metaclass=MetaSingleton):
    """Singleton container to store all images"""

    __images: Dict[ImageTypes, ImageWrapper] = {}

    @classmethod
    def add(cls, image: ImageWrapper):
        """Add the given image to images container"""
        cls.__images[image.image_type] = image
        app_logger.debug("New image with type `%s` registered in the image container", image.image_type.value)

    @classmethod
    def get(cls, image_type: ImageTypes) -> Optional[ImageWrapper]:
        """Get image from container by given image type

        :param image_type: type of image to get
        :return: mage from container with given type if exists
        """
        if image := cls.__images.get(image_type):
            return image
        logging.warning("No image with type % received from container. Does not exist", image_type.value)
        return None

    @classmethod
    def get_all_user_images(cls) -> Generator[ImageWrapper, None, None]:
        """Get generator that returns all images except default"""
        for image in cls.__images.values():
            if image.image_type != ImageTypes.DEFAULT_IMAGE:
                yield image

    @classmethod
    def is_contains_user_images(cls) -> bool:
        """Returns True if there is any user image in the container else False"""
        return any(image for image in cls.__images.values() if image.image_type != ImageTypes.DEFAULT_IMAGE)

    @classmethod
    def get_loaded_image_types(cls) -> list[str]:
        """Get all image types in the container

        :return: all types of images from the container
        """
        return [image.image_type.value for image in cls.__images.values()]
