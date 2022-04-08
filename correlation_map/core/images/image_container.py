from typing import Any, Dict

from core.images.image import Image, ImageTypes
from core.tools.common import MetaSingleton


class ImageContainer(metaclass=MetaSingleton):
    __images: Dict[ImageTypes, Any] = {}

    @classmethod
    def add(cls, image: Image):
        if image.image_type in ImageTypes:
            cls.__images[image.image_type] = image
        raise TypeError(f"Image type {image.image_type} not supported")

