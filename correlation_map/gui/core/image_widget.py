"""Contains image widget class"""
from matplotlib.backends.backend_qt import NavigationToolbar2QT
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QVBoxLayout, QWidget

from correlation_map.core.images.image import ImageWrapper


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
        self.__set_image()

    def __configure_main_layout(self) -> QVBoxLayout:
        """Configure and return vertical layout"""
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        return main_layout

    def __configure_navigation_toolbar(self) -> NavigationToolbar2QT:
        """Configure and return image navigation toolbar"""
        toolbar = NavigationToolbar2QT(self.canvas, self)
        self.main_layout.addWidget(toolbar)
        return toolbar

    def __set_image(self):
        """Set and display current image as plot"""
        self.canvas.axes.imshow(self.image.image)
        self.main_layout.addWidget(self.canvas)
