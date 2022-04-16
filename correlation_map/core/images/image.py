"""Contains all available image types and image wrapper model"""
from enum import Enum
from typing import Optional, Tuple, Union


from matplotlib import pyplot as plt
from numpy import ndarray

from PIL.Image import fromarray, Image

from correlation_map.gui.tools.logger import app_logger


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
        if self.image_type not in ImageTypes:
            raise TypeError(f"Image type `{self.image_type}` not supported")
        self.image: Optional[Image] = plt.imread(self.path) if self.path else None

    def save(self, path: str):
        """Save image by the given path"""
        if self.image is None:
            app_logger.warning("Can not save image with type %s, it's empty", self.image_type.value)
            return
        self.image.save(path)

    @classmethod
    def create_image(cls, image: Union[Image, ndarray], image_type: ImageTypes = None) -> 'ImageWrapper':
        """Create new image by the given arrays

        :param image: arrays of the image to create
        :param image_type: type of the new image
        :return: created image wrapper with the given array and type
        """
        new_image = ImageWrapper(image_type=image_type)
        image_to_set = image
        if isinstance(image, ndarray):
            image_to_set = fromarray(image)
        new_image.image = image_to_set
        return new_image

    @property
    def shape(self) -> Tuple[int, int, int]:
        """Return current images shapes

        :return: tuple of image shapes
        """
        if self.image is None:
            app_logger.warning("Can not get image shapes with type %s, it's empty", self.image_type.value)
            return 0, 0, 0
        return self.image.width, self.image.height, 0

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
