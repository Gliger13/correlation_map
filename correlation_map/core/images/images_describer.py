"""Contains image describer which returns or calculates different image attributes"""
import math
from typing import Tuple

import cv2
import numpy as np

from correlation_map.core.correlation.correlation_maker import CorrelationTypes
from correlation_map.core.images.image import ImageTypes, ImageWrapper


class ImageSelection:
    """ToDo: delete and replace"""
    def __init__(self, x1: int = None, y1: int = None, x2: int = None, y2: int = None):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    @property
    def bottom_right_point(self) -> Tuple[int, int]:
        return self.x1, self.y1

    @property
    def top_left_point(self) -> Tuple[int, int]:
        return self.x2, self.y2


class ImagesDescriber:
    """Contains actions to return or calculate different images attributes"""

    @classmethod
    def find_rotation_angle(cls, src_image: ImageWrapper, dst_image: ImageWrapper,
                            descriptor_lines: int = 0) -> Tuple[float, ImageWrapper]:
        """
        Return the angle of rotation of the img2 relative to img1
        """
        # Use descriptor for detecting the img2 in img1
        orb = cv2.ORB_create()
        kpt1, des1 = orb.detectAndCompute(src_image.image, None)
        kpt2, des2 = orb.detectAndCompute(dst_image.image, None)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)
        matches = sorted(matches, key=lambda x: x.distance)
        # Show both images with the result work of descriptor
        if not descriptor_lines:
            descriptor_lines = 0
        elif descriptor_lines > len(matches):
            descriptor_lines = matches
        output_image = cv2.drawMatches(src_image.image, kpt1, dst_image.image,
                                       kpt2, matches[:descriptor_lines], None, flags=2)
        descriptor_image = ImageWrapper.create_image(output_image, ImageTypes.DETECTED_IMAGE)
        # Calculation angle
        src_pts = np.float32([kpt1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kpt2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

        matrix, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        theta = - math.atan2(matrix[0, 1], matrix[0, 0]) * 180 / math.pi
        return theta, descriptor_image

    @classmethod
    def find_image_points(cls, source_image: ImageWrapper, destination_image: ImageWrapper,
                          type_of_correlation: CorrelationTypes) -> ImageSelection:
        res = cv2.matchTemplate(source_image.image, destination_image.image, type_of_correlation.correlation_cv2_type)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        h, w, _ = destination_image.image.shape

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        image_selection = ImageSelection()
        if type_of_correlation.correlation_cv2_type in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            image_selection.x1, image_selection.y1 = min_loc
        else:
            image_selection.x1, image_selection.y1 = max_loc
        image_selection.x2, image_selection.y2 = image_selection.x1 + w, image_selection.y1 + h
        return image_selection
