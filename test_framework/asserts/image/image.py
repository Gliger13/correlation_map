import numpy as np

from core.image import Image, ImageBuilder


def check_gray_transformation(source_image: Image, expected_gray_image: Image):
    gray_image = ImageBuilder().transform_image_to_gray(source_image)
    assert_msg = "Image after converting to gray is not the same"
    assert np.array_equal(gray_image.image, expected_gray_image.image), assert_msg
