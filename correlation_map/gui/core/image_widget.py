"""Contains image widget class"""
from dataclasses import dataclass
from typing import Dict, Generator, Optional, Tuple

from matplotlib import pyplot as plt
from matplotlib.backend_bases import MouseEvent
from matplotlib.backends.backend_qt import NavigationToolbar2QT
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from matplotlib.widgets import RectangleSelector
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QSpinBox, QVBoxLayout, QWidget

from correlation_map.core.images.image import ImageWrapper
from correlation_map.gui.tools.common import log_configuration_process
from correlation_map.gui.tools.logger import app_logger


@dataclass
class ImageSelectedRegion:
    """Dataclass for image selection region"""
    x_1: int
    y_1: int
    x_2: int
    y_2: int

    @property
    def height(self) -> int:
        """Return selected region height"""
        return abs(self.y_2 - self.y_1)

    @property
    def width(self) -> int:
        """Return selected region width"""
        return abs(self.x_2 - self.x_1)

    @property
    def left_bottom_point(self) -> Tuple[int, int]:
        """Return left bottom coordinates of the selected region"""
        return min(self.x_1, self.x_2), min(self.y_1, self.y_2)

    @property
    def attributes_dict(self) -> Dict[str, int]:
        """Return dict of rectangle coordinates"""
        return {"x_1": self.x_1, "y_1": self.y_1, "x_2": self.x_2, "y_2": self.y_2}

    @property
    def items(self) -> Generator[Tuple[str, int], None, None]:
        """Return generator that returns items of selected rectangle coordinates"""
        for item in self.attributes_dict.items():
            yield item


class MplCanvas(FigureCanvasQTAgg):
    """Figure canvas class inheritance to display image as plot"""

    def __init__(self, width: int = 5, height: int = 4, dpi: int = 100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)


class ImageWidget(QWidget):
    """Image widget wrapper for displaying an image as plot and plot tools"""

    def __init__(self, image: ImageWrapper):
        """
        :param image: image wrapper to attach to widget
        """
        super().__init__()
        self.image = image
        self.canvas = MplCanvas(width=5, height=4, dpi=100)
        self.main_layout = self.__configure_main_layout()
        self.tool_bar = self.__configure_navigation_toolbar()
        self._set_image()

    @log_configuration_process
    def __configure_main_layout(self) -> QVBoxLayout:
        """Configure and return vertical layout"""
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        return main_layout

    @log_configuration_process
    def __configure_navigation_toolbar(self) -> NavigationToolbar2QT:
        """Configure and return image navigation toolbar"""
        toolbar = NavigationToolbar2QT(self.canvas, self)
        self.main_layout.addWidget(toolbar)
        return toolbar

    def _set_image(self):
        """Set and display current image as plot"""
        self.canvas.axes.imshow(self.image.image)
        self.main_layout.addWidget(self.canvas)


class ImageWidgetWithSelector(ImageWidget):
    """Wrapper for image widget with rectangle selector on image graph"""

    def __init__(self, image: ImageWrapper):
        """
        :param image: image wrapper to attach to widget
        """
        super().__init__(image)
        x_max_value, y_max_value, _ = self.image.shape
        self.selected_region = ImageSelectedRegion(x_1=0, y_1=0, x_2=x_max_value, y_2=y_max_value)
        self._selected_region_layout = self._configure_selected_region_layout()
        self.selected_region_spin_boxes = self._configure_selected_region_spin_boxes()

        self._last_drawn_rectangle: Optional[Rectangle] = None

    def _update_spin_boxes(self):
        """Update all spin boxes with the current values from the selected region"""
        for spin_box, (_, attribute_value) in zip(self.selected_region_spin_boxes, self.selected_region.items):
            spin_box.setValue(attribute_value)

    def _draw_rectangle_on_selected_region(self):
        """Draw rectangle in the current selected region and remove old one"""
        if self._last_drawn_rectangle:
            self._last_drawn_rectangle.remove()
        rectangle_to_draw = Rectangle(self.selected_region.left_bottom_point, self.selected_region.width,
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
        self.canvas.axes.imshow(self.image.image)
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
        max_values = (self.image.shape[0], self.image.shape[1], self.image.shape[0], self.image.shape[1])

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
