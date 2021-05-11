from enum import Enum

from core.correlation.correlation_map import CorrelationMap
from core.images.image import Image, ImageTypes
from core.images.image_builder import ImageBuilder
from core.images.image_container import ImageContainer
from core.images.images_describer import ImagesDescriber
from core.user.user import UserActions


class CorrelationMapProcessBuilder:
    def __init__(self, user: UserActions):
        self.user = user
        self.images_container = ImageContainer()

        self.current_src_image = None
        self.current_dst_image = None

    def _load_user_images(self):
        source_image = Image(self.user.image1_path, ImageTypes.SOURCE_IMAGE)
        self.images_container.add(source_image)
        self.current_src_image = source_image

        destination_image = Image(self.user.image2_path, ImageTypes.DESTINATION_IMAGE)
        self.images_container.add(destination_image)
        self.current_dst_image = destination_image

    def _scale_image(self):
        top_left_point, bottom_right_point = self.user.get_scale_points()
        top_left_point, bottom_right_poin = (50, 50), (150, 150)
        scaled_image = ImageBuilder.scale_image(self.current_src_image, top_left_point, bottom_right_point)
        self.images_container.add(scaled_image)
        self.current_src_image = scaled_image

    def _rotate_image(self):
        rotate_angle, detected_image = ImagesDescriber.find_rotation_angle(self.current_src_image,
                                                                           self.current_dst_image)
        self.images_container.add(detected_image)

        rotated_image = ImageBuilder.rotate_image(self.current_dst_image, rotate_angle)
        self.images_container.add(rotated_image)

    def _find_and_cut(self):
        image_with_rectangle, cropped_image = ImageBuilder.find_and_cut(self.current_src_image,
                                                                        self.current_dst_image,
                                                                        self.user.correlation)
        self.images_container.add(image_with_rectangle)
        self.images_container.add(cropped_image)
        self.current_dst_image = cropped_image

    def _build_correlation_map(self) -> CorrelationMap:
        self.user.delim = 4  # !!!
        correlation_map = CorrelationMap(self.current_src_image, self.current_dst_image,
                                         self.user.correlation, self.user.delim).build_correlation_map()
        return correlation_map

    def build_correlation_map(self) -> CorrelationMap:
        self._load_user_images()
        self._scale_image()
        self._rotate_image()
        self._find_and_cut()
        return self._build_correlation_map()
