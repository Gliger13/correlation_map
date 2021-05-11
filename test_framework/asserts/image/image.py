import math

import numpy as np

from core.images.image import Image
from core.images.image_builder import ImageBuilder
from core.images.images_describer import ImagesDescriber


def check_gray_transformation(source_image: Image, expected_image: Image):
    gray_image = ImageBuilder.transform_image_to_gray(source_image)
    assert_msg = "Image after converting to gray is not the same"
    assert np.array_equal(gray_image.image, expected_image.image), assert_msg


def check_rotate_image(source_image: Image, expected_image: Image):
    rotated_image = ImageBuilder.rotate_image(source_image, 90.31054357218517)
    assert_msg = "Image after rotation is not the same as expected"
    assert np.allclose(rotated_image.image, expected_image.image, atol=1, rtol=1), assert_msg


def check_find_image_rotation_angle(source_image: Image, expected_image: Image):
    angle, _ = ImagesDescriber.find_rotation_angle(source_image, expected_image)
    assert_msg = "Image rotation is not same as expected"
    assert math.isclose(angle, 90, rel_tol=1), assert_msg
