from core.images.image import Image, ImageTypes


class ImageContainer:
    def __init__(self, images: dict = None):
        self.images = images if images else {}

    def add(self, image: Image):
        if image.image_type in ImageTypes:
            self.images[image.image_type] = image
        raise TypeError(f"Image type {image.image_type} not supported")

