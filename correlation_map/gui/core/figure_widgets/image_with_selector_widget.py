"""Image with selector widget

Image widget wrapper to allow user to select image region to crop.
"""
from typing import Optional, Tuple

from matplotlib import pyplot as plt
from matplotlib.backend_bases import MouseEvent
from matplotlib.patches import Rectangle
from matplotlib.widgets import RectangleSelector
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QSpinBox, QWidget

from correlation_map.core.models.figures.image import ImageWrapper
from correlation_map.core.models.image_selected_region import ImageSelectedRegion
from correlation_map.gui.core.figure_widgets.image_widget import ImageWidget
from correlation_map.gui.tools.common import log_configuration_process
from correlation_map.gui.tools.logger import app_logger


class ImageWithSelectorWidget(ImageWidget):
    """Wrapper for image widget with rectangle selector on image graph"""

    def __init__(self, image: ImageWrapper):
        """
        :param image: image wrapper to attach to widget
        """
        super().__init__(image)

        self.selected_region = self._get_default_image_selected_region()
        self._selected_region_layout = self._configure_selected_region_layout()
        self.selected_region_spin_boxes = self._configure_selected_region_spin_boxes()

        self._last_drawn_rectangle: Optional[Rectangle] = None

    def _get_default_image_selected_region(self) -> ImageSelectedRegion:
        """Get the whole image as default image selected region"""
        y_max_value, x_max_value, _ = self.figure.shape
        return ImageSelectedRegion(x_1=0, y_1=0, x_2=x_max_value, y_2=y_max_value)

    def _update_spin_boxes(self):
        """Update all spin boxes with the current values from the selected region"""
        for spin_box, (_, attribute_value) in zip(self.selected_region_spin_boxes, self.selected_region.items):
            spin_box.setValue(attribute_value)

    def _draw_rectangle_on_selected_region(self):
        """Draw rectangle in the current selected region and remove old one"""
        if self._last_drawn_rectangle:
            self._last_drawn_rectangle.remove()
        rectangle_to_draw = Rectangle(self.selected_region.bottom_left_point, self.selected_region.width,
                                      self.selected_region.height, linewidth=1, edgecolor='r', facecolor='none')
        self.canvas.axes.add_patch(rectangle_to_draw)
        self._last_drawn_rectangle = rectangle_to_draw

    def _on_select(self, press_click: MouseEvent, released_click: MouseEvent):
        """Event when rectangle is selected

        After selecting the rectangle:
        1) Update current coordinates of the selected region
        2) Update spin boxes widgets with new values
        3) Delete and draw a rectangle in the selected region

        :param press_click: mouse event on mouse clicked
        :param released_click: mouse event on mouse released
        """
        self.selected_region = ImageSelectedRegion(
            x_1=round(press_click.xdata), y_1=round(press_click.ydata),
            x_2=round(released_click.xdata), y_2=round(released_click.ydata))
        self._update_spin_boxes()
        self._draw_rectangle_on_selected_region()
        app_logger.debug("User selected image region - %s", self.selected_region)

    def _set_image(self):
        """Set and display current image as plot. Add rectangle selector."""
        app_logger.debug("Setting image in the image widget with selector")
        self.canvas.axes.imshow(self.figure.image)
        rectangle_selector_event = RectangleSelector(self.canvas.axes, self._on_select, drawtype='box', button=[1, 3])
        plt.connect('key_press_event', rectangle_selector_event)
        self.main_layout.addWidget(self.canvas)

    @log_configuration_process
    def _configure_selected_region_layout(self) -> QGridLayout:
        """Configure and return selected region layout"""
        grid_layout = QGridLayout()
        self.main_layout.addLayout(grid_layout)
        return grid_layout

    @log_configuration_process
    def _configure_selected_region_spin_boxes(self) -> Tuple[QSpinBox, ...]:
        """Configure and return spin boxes for selected region coordinates"""
        widget_grid_places = (0, 0), (0, 1), (1, 0), (1, 1)
        y_max_value, x_max_value, _ = self.figure.shape
        max_values = x_max_value, y_max_value, x_max_value, y_max_value

        configured_widgets: list[tuple[QLabel, QSpinBox]] = []
        for attribute, max_value, place in zip(self.selected_region.items, max_values, widget_grid_places):
            attribute_name, attribute_value = attribute

            attribute_layout = QHBoxLayout()

            label_widget = QWidget()
            attribute_label = QLabel(label_widget)
            attribute_label.setText(f"{attribute_name.replace('_', '')}: ")
            attribute_label.setAlignment(Qt.AlignCenter)
            attribute_layout.addWidget(attribute_label)

            attribute_spin_box = QSpinBox()
            attribute_spin_box.setRange(0, max_value)
            attribute_spin_box.setValue(attribute_value)
            attribute_spin_box.setAlignment(Qt.AlignCenter)
            attribute_layout.addWidget(attribute_spin_box)

            configured_widgets.append((attribute_label, attribute_spin_box))
            self._selected_region_layout.addLayout(attribute_layout, place[0], place[1])
        return tuple((configured_widget[1] for configured_widget in configured_widgets))
