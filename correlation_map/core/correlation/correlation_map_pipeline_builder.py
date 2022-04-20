"""Module contains correlation map building"""
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Final, Generator, Optional

from correlation_map.core.config.correlation import CorrelationConfiguration
from correlation_map.core.correlation.correlation_map import CorrelationMap
from correlation_map.core.images.image import ImageTypes, ImageWrapper
from correlation_map.core.images.image_builder import ImageBuilder
from correlation_map.core.images.image_container import ImageContainer
from correlation_map.core.images.images_describer import ImagesDescriber
from correlation_map.gui.tools.logger import app_logger


class CorrelationStageAttributes(Enum):
    """Contains all possible correlation map building stages and their parameters"""

    START = "start", "Waiting for user to click a button to start correlation map building", 0
    LOADING = "loading", "Loading source and destination images", 0
    SCALE_IMAGE = "scaling image", "Scaling source image according to user choice", 1
    FIND_ROTATE_ANGLE = "finding rotate angle", "Finding rotate angle between source and destination images", 3
    ROTATE_IMAGE = "rotating destination image", "Rotating destination image", 2
    FIND_IMAGE = "find source image", "Finding source image in destination images", 3
    MARK_FOUND_IMAGE = "mark found image", "Marking found source image in destination image", 2
    CROP_FOUND_IMAGE = "croup found image", "Cropping found source image in destination image", 2
    BUILD_CORRELATION_MAP = "build correlation map", "Building correlation map", 20
    END = "end", "Correlation map built", 0

    def __init__(self, status: str, message: str, weight: int):
        """
        :param status: short name of the stage
        :param message: full stage description
        :param weight: represents approximate time estimation or difficult coefficient of the stage. Used to know
            which stage takes more time to complete
        """
        self.status = status
        self.message = message
        self.weight = weight


@dataclass
class CurrentCorrelationStage:
    """Represents correlation pipeline current stage

    Represents the correlation pipeline current or running stage. Describes their progress, attributes,
    and errors if any.
    """
    stage_attributes: CorrelationStageAttributes
    pipeline_progress: int
    error: Optional[str] = None


class CorrelationBuildingPipeline:
    """Represents a single correlation building chain of the stages"""

    MAX_STEPS_AMOUNT: Final[int] = 100

    def __init__(self, correlation_configuration: CorrelationConfiguration):
        """
        :param correlation_configuration: filled correlation configuration
        """
        self._correlation_configuration = correlation_configuration
        self.planed_stages = self.__get_planed_stages(correlation_configuration)
        self.current_stage_number: int = 0
        self.progress: int = 0

    def __iter__(self):
        """Correlation building pipeline stages iterator

        Iterator returns fresh not started correlation pipeline. Sets progress and current stage number to 0.
        """
        self.current_stage_number = 0
        self.progress = 0
        return self

    def __next__(self) -> CurrentCorrelationStage:
        """Switch to next correlation building stage and return it

        Update correlation pipeline current stage number. Update pipeline progress number.
        :return: next correlation building stage
        """
        if len(self.planed_stages) < self.current_stage_number:
            raise StopIteration
        if self.current_stage_attributes == self.planed_stages[-1]:
            self.progress = self.MAX_STEPS_AMOUNT
        else:
            self.progress += self.current_pipeline_stage_step
        self.current_stage_number += 1
        app_logger.info("Correlation pipeline: Current stage - %s, pipeline progress - %s/%s",
                        self.current_stage_attributes.status, self.progress, self.MAX_STEPS_AMOUNT)
        return self.current_stage

    @property
    def current_stage(self) -> CurrentCorrelationStage:
        """Returns current correlation pipeline stage dataclass"""
        return CurrentCorrelationStage(self.current_stage_attributes, self.progress)

    @property
    def current_stage_attributes(self) -> CorrelationStageAttributes:
        """Returns current correlation pipeline stage attributes"""
        return self.planed_stages[self.current_stage_number]

    @property
    def current_pipeline_stage_step(self) -> int:
        """Returns current pipeline stage step

        Returns the current step number of the pipeline stage, which represents the progress the pipeline will make
        after the stage completes.

        :return: current pipeline stage progress amount
        """
        return round(self.current_stage_attributes.weight * self.pipeline_stage_weight)

    @property
    def pipeline_stage_weight(self) -> float:
        """Returns approximate pipeline stage weight coefficient

        Calculates and returns approximate stage weight coefficient, which represent the progress the current pipeline
        with a specific set of stages will make after the stage with weight = 1.

        :return: pipeline stage weight coefficient
        """
        weight_sum = sum(stage.weight for stage in self.planed_stages)
        return self.MAX_STEPS_AMOUNT / weight_sum

    @classmethod
    def __get_planed_stages(cls, correlation_settings: CorrelationConfiguration) -> list[CorrelationStageAttributes]:
        """Returns list of planed stages from the given correlation settings"""
        planned_stages: list[CorrelationStageAttributes] = [
            CorrelationStageAttributes.START,
            CorrelationStageAttributes.LOADING,
        ]
        if correlation_settings.chose_important_part:
            planned_stages.append(
                CorrelationStageAttributes.SCALE_IMAGE)
        if correlation_settings.auto_rotate:
            planned_stages.extend([
                CorrelationStageAttributes.FIND_ROTATE_ANGLE,
                CorrelationStageAttributes.ROTATE_IMAGE])
        if correlation_settings.auto_rotate:
            planned_stages.extend([
                CorrelationStageAttributes.FIND_IMAGE,
                CorrelationStageAttributes.MARK_FOUND_IMAGE,
                CorrelationStageAttributes.CROP_FOUND_IMAGE])
        planned_stages.extend([
            CorrelationStageAttributes.BUILD_CORRELATION_MAP,
            CorrelationStageAttributes.END])
        return planned_stages


class CorrelationMapPipelineBuilder:
    """Correlation map pipeline builder, which runs correlation pipeline with the given correlation settings"""

    def __init__(self, correlation_settings: CorrelationConfiguration):
        """
        :param correlation_settings: filled correlation setting to pass to correlation pipeline and sub-pipelines
        """
        self.correlation_settings = correlation_settings
        self.correlation_pipeline = iter(CorrelationBuildingPipeline(correlation_settings))

        self.current_source_image: Optional[ImageWrapper] = None
        self.current_destination_image: Optional[ImageWrapper] = None

    def _crop_image(self) -> Generator[CurrentCorrelationStage, None, None]:
        """Sub-pipeline to scale source image

        1) Crop source image
        2) Add cropped image to the image container
        3) Set cropped source image as current source image

        :return: generator that returns current correlation pipeline stage
        """
        app_logger.info("Correlation pipeline: Scaling source image according to user choice")
        yield next(self.correlation_pipeline)
        scaled_image = ImageBuilder.crop_image(
            self.current_source_image, self.correlation_settings.selected_image_region.top_left_point,
            self.correlation_settings.selected_image_region.bottom_right_point)
        ImageContainer.add(scaled_image)
        self.current_source_image = scaled_image
        app_logger.info("Correlation pipeline: Source image scaled")

    def _rotate_image(self) -> Generator[CurrentCorrelationStage, None, None]:
        """Sub-pipeline to rotate destination image

        1) Find rotation angle between source and destination image
        2) Create image with source and destination images with detected lines
        3) Rotate destination image with the calculated angle
        4) Add detected and rotated image to image container
        5) Set rotated image as current destination image

        :return: generator that returns current correlation pipeline stage
        """
        app_logger.info("Correlation pipeline: Rotating destination image")
        yield next(self.correlation_pipeline)
        rotate_angle, detected_image = ImagesDescriber.find_rotation_angle(
            self.current_source_image, self.current_destination_image)
        ImageContainer.add(detected_image)
        yield next(self.correlation_pipeline)
        rotated_image = ImageBuilder.rotate_image(self.current_destination_image, rotate_angle)
        ImageContainer.add(rotated_image)
        self.current_destination_image = rotated_image
        app_logger.info("Correlation pipeline: Destination rotated")

    def _find_and_crop(self) -> Generator[CurrentCorrelationStage, None, None]:
        """Sub-pipeline to find and crop destination image

        1) Find image region in the destination image that represents the source image
        2) Mark found region in the destination image
        3) Crop found region in the destination image
        4) Add marked and cropped image to image container
        5) Set cropped image as current destination image

        :return: generator that returns current correlation pipeline stage
        """
        app_logger.info("Correlation pipeline: Finding source image in the destination image")
        yield next(self.correlation_pipeline)
        image_selection = ImagesDescriber.find_image_points(
            self.current_source_image, self.current_destination_image, self.correlation_settings.correlation_type)
        yield next(self.correlation_pipeline)
        marked_image = ImageBuilder.mark_found_image(self.current_destination_image, image_selection)
        ImageContainer.add(marked_image)
        yield next(self.correlation_pipeline)
        cropped_image = ImageBuilder.crop_found_image(self.current_destination_image, image_selection)
        ImageContainer.add(cropped_image)
        self.current_destination_image = cropped_image
        app_logger.info("Correlation pipeline: Source image found")

    def _build_correlation_map(self) -> Generator[CurrentCorrelationStage, None, None]:
        """Sub-pipeline to build correlation map

        Create correlation map and add it to the image container

         :return: generator that returns current correlation pipeline stage
         """
        app_logger.info("Correlation pipeline: Start correlation map calculations")
        yield next(self.correlation_pipeline)
        correlation_map = CorrelationMap(
            self.current_source_image,
            self.current_destination_image,
            self.correlation_settings.correlation_type,
            self.correlation_settings.correlation_pieces_count,
        ).build_correlation_map()
        ImageContainer.add(correlation_map)
        app_logger.info("Correlation pipeline: Correlation map calculated")

    def start_correlation_building_pipeline(self) -> Generator[CurrentCorrelationStage, None, None]:
        """Start correlation building pipeline

        :return: generator that returns current correlation pipeline stage
        """
        app_logger.info("Correlation pipeline: Start correlation building pipeline")
        yield next(self.correlation_pipeline)

        self.current_source_image = ImageContainer.get(ImageTypes.SOURCE_IMAGE)
        self.current_destination_image = ImageContainer.get(ImageTypes.DESTINATION_IMAGE)

        sub_pipelines: list[Callable[[], Generator[CurrentCorrelationStage, None, None]]] = []
        if self.correlation_settings.chose_important_part:
            sub_pipelines.append(self._crop_image)
        if self.correlation_settings.auto_rotate:
            sub_pipelines.append(self._rotate_image)
        if self.correlation_settings.auto_find:
            sub_pipelines.append(self._find_and_crop)
        sub_pipelines.append(self._build_correlation_map)

        for sub_pipeline in sub_pipelines:
            for stage in sub_pipeline():
                yield stage
        yield next(self.correlation_pipeline)

        app_logger.info("Correlation pipeline: pipeline finished")
