"""Contains image describer which returns or calculates different image attributes"""
import math

import cv2
import numpy as np

from correlation_map.core.config.correlation import CorrelationTypes
from correlation_map.core.config.figure_types import FigureType
from correlation_map.core.models.figures.image import ImageWrapper
from correlation_map.core.models.image_selected_region import ImageSelectedRegion


class ImagesDescriber:
    """Contains actions to return or calculate different images attributes"""

    @classmethod
    def find_rotation_angle(cls, source_image: ImageWrapper, destination_image: ImageWrapper,
                            descriptor_lines: int = 0) -> tuple[float, ImageWrapper]:
        """
        Return the angle of rotation of the source image relative to destination image
        """
        # Use descriptor for detecting the source image in the destination image
        orb = cv2.ORB_create()
        src_image_key_points, src_image_descriptors = orb.detectAndCompute(source_image.image, None)
        dst_image_key_points, dst_image_descriptors = orb.detectAndCompute(destination_image.image, None)
        brute_force_match = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = brute_force_match.match(src_image_descriptors, dst_image_descriptors)
        matches = sorted(matches, key=lambda match: match.distance)
        # Show both images with the result work of descriptor
        if not descriptor_lines:
            descriptor_lines = 0
        elif descriptor_lines > len(matches):
            descriptor_lines = matches
        output_image = cv2.drawMatches(
            img1=source_image.image,
            keypoints1=src_image_key_points,
            img2=destination_image.image,
            keypoints2=dst_image_key_points,
            matches1to2=matches[:descriptor_lines],
            outImg=None,
            flags=2,
        )
        descriptor_image = ImageWrapper.create_image(output_image, FigureType.DETECTED_IMAGE)
        # Calculation angle
        src_pts = np.float32([src_image_key_points[match.queryIdx].pt for match in matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([dst_image_key_points[match.trainIdx].pt for match in matches]).reshape(-1, 1, 2)

        matrix, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        theta = - math.atan2(matrix[0, 1], matrix[0, 0]) * 180 / math.pi
        return theta, descriptor_image

    @classmethod
    def find_image_points(cls, source_image: ImageWrapper, destination_image: ImageWrapper,
                          type_of_correlation: CorrelationTypes) -> ImageSelectedRegion:
        """Find image points of the source image in the destination image

        :param source_image: source image to find in the destination
        :param destination_image: destination image to find image area of
            source image
        :param type_of_correlation: correlation type to use while matching
            source image in the destination one
        :return: image region coordinates of the source image in the
            destination image
        """
        res = cv2.matchTemplate(destination_image.image, source_image.image, type_of_correlation.correlation_cv2_type)
        _, _, min_loc, max_loc = cv2.minMaxLoc(res)
        height, weight, _ = destination_image.image.shape

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if type_of_correlation in [CorrelationTypes.TM_SQDIFF, CorrelationTypes.TM_SQDIFF_NORMED]:
            x_1, y_1 = min_loc
        else:
            x_1, y_1 = max_loc
        x_2, y_2 = x_1 + height, y_1 + weight
        return ImageSelectedRegion(x_1=x_1, y_1=y_1, x_2=x_2, y_2=y_2)
