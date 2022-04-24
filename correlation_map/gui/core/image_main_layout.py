"""Contains vertical layout wrapper for all image widgets"""
from typing import Mapping, Type

import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from correlation_map.core.config.figure_types import FigureType
from correlation_map.core.models.figures.base_figure import BaseFigure
from correlation_map.core.models.figures.correlation_map import CorrelationMap
from correlation_map.core.models.figures.image import ImageWrapper
from correlation_map.core.models.figures.figure_container import FigureContainer
from correlation_map.gui.core.figure_widgets.base_figure_widget import BaseFigureWidget
from correlation_map.gui.core.figure_widgets.correlation_map_widget import CorrelationMapWidget
from correlation_map.gui.core.figure_widgets.image_widget import ImageWidget
from correlation_map.gui.core.image_chooser import ImageChooserComboBox
from correlation_map.gui.tools.logger import app_logger

FIGURE_AND_WIDGET_MAP: Mapping[Type[BaseFigure], Type[BaseFigureWidget]] = {
    ImageWrapper: ImageWidget,
    CorrelationMap: CorrelationMapWidget,
}


class ImageMainLayout(QVBoxLayout):
    """Vertical layout for all image widgets"""

    def __init__(self, widget_to_attach: QWidget):
        """
        :param widget_to_attach: widget for attaching a layout
        """
        super().__init__(widget_to_attach)
        self._first_horizontal_layout = self.__configure_first_horizontal_layout()
        self._first_left_horizontal_layout = self.__configure_first_left_horizontal_layout()
        self.first_right_horizontal_layout = self.__configure_first_right_horizontal_layout()
        self.image_chooser = self.__configure_image_chooser()

        # Configure active buttons
        self.__open_in_new_window_button_widget = QWidget()
        self.open_in_new_window_button = self.__configure_open_in_new_window_button(
            self.__open_in_new_window_button_widget)
        self.__move_to_new_window_widget = QWidget()
        self.move_to_new_window_button = self.__configure_move_to_new_window_button(self.__move_to_new_window_widget)
        self.__close_button_widget = QWidget()
        self.close_button = self.__configure_close_button(self.__close_button_widget)

        self.image_widget = self.__configure_default_figure_widget()

    def set_image(self, force_update: bool = False):
        """Set new image widget by type from the image chooser box

        Get image type from the current image chooser combo box and get image wrapper from the image container using it.
        Replace the current image widget with a new widget with the image wrapper from the image container.

        :param force_update: if True then update the image widget even if it is of the same type as the current one
        """
        user_choice = self.image_chooser.currentText()
        app_logger.debug("User chosen `%s` in the image chooser", user_choice)
        chosen_image_type = FigureType.get_by_name(user_choice)
        if not chosen_image_type:
            app_logger.warning("Chosen wrong image type by image chooser box. Selected `%s`. Ignoring", user_choice)
            return None
        if not force_update and self.image_widget.figure.figure_type == chosen_image_type:
            app_logger.debug("The selected image with type `%s` is the same as the current one. Ignoring",
                             self.image_widget.figure.figure_type.value)
            return None
        app_logger.info("Setting image with type `%s`", chosen_image_type.value)
        figure = FigureContainer.get(chosen_image_type)
        if not figure:
            app_logger.error("Can't get and set chosen figure with type %s by image chooser from the image container",
                             chosen_image_type.value)
            return None
        self.removeWidget(self.image_widget)

        if figure_widget_class := FIGURE_AND_WIDGET_MAP.get(type(figure)):
            widget_to_set = figure_widget_class(figure)
        else:
            app_logger.warning("Cannot set new figure widget. Unknown figure type. Given - `%s`, Expected on of `%s`",
                               type(figure), FIGURE_AND_WIDGET_MAP.keys())
            return None

        self.addWidget(widget_to_set)
        self.image_widget = widget_to_set
        app_logger.info("Figure with type `%s` was set as figure widget", chosen_image_type.value)
        return None

    def __configure_first_horizontal_layout(self) -> QHBoxLayout:
        """Configure and return first horizontal layout for image chooser text, image chooser and close button"""
        first_horizontal_layout = QHBoxLayout()
        self.addLayout(first_horizontal_layout)
        return first_horizontal_layout

    def __configure_first_left_horizontal_layout(self) -> QHBoxLayout:
        """Configure and return left first horizontal layout for image chooser text, image chooser and close button"""
        first_left_horizontal_layout = QHBoxLayout()
        self._first_horizontal_layout.addLayout(first_left_horizontal_layout)
        self._first_horizontal_layout.setStretchFactor(first_left_horizontal_layout, 1)
        return first_left_horizontal_layout

    def __configure_first_right_horizontal_layout(self) -> QHBoxLayout:
        """Configure and return right first horizontal layout for image chooser text, image chooser and close button"""
        first_right_horizontal_layout = QHBoxLayout()
        first_right_horizontal_layout.setAlignment(Qt.AlignRight)
        self._first_horizontal_layout.addLayout(first_right_horizontal_layout)
        self._first_horizontal_layout.setStretchFactor(first_right_horizontal_layout, 1)
        return first_right_horizontal_layout

    def __configure_image_chooser(self) -> ImageChooserComboBox:
        """Configure and return image chooser combo box"""
        image_chooser = ImageChooserComboBox()
        text_label = QLabel()
        text_label.setText("Displayed image: ")
        self._first_left_horizontal_layout.addWidget(text_label)
        self._first_left_horizontal_layout.addWidget(image_chooser, 1)
        image_chooser.activated.connect(self.set_image)
        app_logger.debug("Image chooser box configured")
        return image_chooser

    def __configure_close_button(self, close_button_widget: QWidget) -> QPushButton:
        """Configure and return close image layout button

        :param close_button_widget: widget for attaching a button
        :return: configured close button
        """
        app_logger.debug("Configuring close image layout button")
        close_button = QPushButton(close_button_widget)
        close_button.setText("Close")
        self.first_right_horizontal_layout.addWidget(close_button)
        return close_button

    def __configure_open_in_new_window_button(self, open_in_new_window_widget: QWidget) -> QPushButton:
        """Configure and return open image in the new window button

        :param open_in_new_window_widget: widget for attaching a button
        :return: configured open image in the new window button
        """
        app_logger.debug("Configuring open in new window button")
        open_in_new_window_button = QPushButton(open_in_new_window_widget)
        open_in_new_window_button.setText("Open in new window")
        self.first_right_horizontal_layout.addWidget(open_in_new_window_button)
        return open_in_new_window_button

    def __configure_move_to_new_window_button(self, move_to_new_window_widget: QWidget) -> QPushButton:
        """Configure and return move image to new window button

        :param move_to_new_window_widget: widget for attaching a button
        :return: configured move image to new window
        """
        app_logger.debug("Configuring move to new window button")
        move_to_new_window_button = QPushButton(move_to_new_window_widget)
        move_to_new_window_button.setText("Move to new window")
        self.first_right_horizontal_layout.addWidget(move_to_new_window_button)
        return move_to_new_window_button

    def __configure_default_figure_widget(self) -> ImageWidget:
        """Configure and return image widget with default image"""
        image = FigureContainer.get(FigureType.DEFAULT_IMAGE)
        if not image:
            app_logger.error("Can't get and set default image from the image container. "
                             "Creating new white image for that")
            white_image_array = np.full((500, 500, 3), 255, dtype=np.uint8)
            image = ImageWrapper.create_image(white_image_array, FigureType.DEFAULT_IMAGE)
            FigureContainer.add(image)
        image_widget = ImageWidget(image)
        self.addWidget(image_widget)
        app_logger.debug("Image widget with default image has been set")
        return image_widget
