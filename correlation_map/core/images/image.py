from enum import Enum
from typing import Tuple

import cv2


class ImageTypes(Enum):
    SOURCE_IMAGE = "source_image"
    DESTINATION_IMAGE = "destination_image"
    SCALED_IMAGE = "scaled_image"
    DETECTED_IMAGE = "detected_image"
    ROTATED_IMAGE = "rotated_image"
    FOUND_IMAGE = "found_image"
    FOUND_AND_CROPPED = "found_and_cropped_image"
    CORRELATION_MAP = "correlation_map"


class Image:
    def __init__(self, path: str = None, image_type: ImageTypes = None):
        self.path = path
        self.image_type = image_type
        self.image = self.__load_image()

    def __load_image(self):
        return cv2.imread(self.path)

    def save(self, path: str):
        pass

    @classmethod
    def create_image(cls, image, image_type: ImageTypes = None):
        new_image = Image(image_type=image_type)
        new_image.image = image
        return new_image

    @property
    def shape(self) -> Tuple[int, int, int]:
        return self.image.shape

    def show(self):
        cv2.imshow("Test image", self.image)
