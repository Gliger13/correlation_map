"""Base figure widget

Contains base figure widget to implement. Configures and displays matplotlib
figure as widget.
"""
from abc import abstractmethod

from matplotlib.backends.backend_qt import NavigationToolbar2QT
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from PyQt5.QtWidgets import QVBoxLayout, QWidget

from correlation_map.core.models.figures.base_figure import BaseFigure
from correlation_map.gui.tools.common import log_configuration_process


class BaseFigureWidget(QWidget):
    """Figure widget to configure and display figure as widget"""

    def __init__(self, figure: BaseFigure):
        """
        :param figure: figure to set as widget
        """
        super().__init__()
        self.figure = figure
        self.canvas = self._get_canvas()
        self.main_layout = self.__configure_main_layout()
        self.tool_bar = self.__configure_navigation_toolbar()
        self._set_image()

    @abstractmethod
    def _get_canvas(self) -> FigureCanvasQTAgg:
        """Abstract method to create, configure and return canvas figure"""

    def _set_image(self):
        """Set and display current figure as matplotlib plot"""
        self.figure.configure_figure_axes(self.canvas.axes)
        self.main_layout.addWidget(self.canvas)

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
