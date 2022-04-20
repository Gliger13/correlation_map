"""Module contains widget for correlation map 3d plot"""
from matplotlib.backends.backend_qt import NavigationToolbar2QT
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QVBoxLayout, QWidget

from correlation_map.core.correlation.correlation_map import CorrelationMap
from correlation_map.gui.tools.common import log_configuration_process


class Mpl3dCanvas(FigureCanvasQTAgg):
    """Figure canvas class inheritance to display image as 3d plot"""

    def __init__(self, width: int = 5, height: int = 4, dpi: int = 100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111, projection='3d')
        super().__init__(fig)


class CorrelationMapWidget(QWidget):
    """Image widget wrapper for displaying an image as plot and plot tools"""

    def __init__(self, correlation_map: CorrelationMap):
        """
        :param correlation_map: correlation map to attach to the widget
        """
        super().__init__()
        self.correlation_map = correlation_map
        self.canvas = Mpl3dCanvas(width=5, height=4, dpi=100)
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
        """Set and display current correlation map as 3d plot"""
        x_array = []
        y_array = []
        z_array = []
        for x, row in enumerate(self.correlation_map.correlation_map):
            for y, _ in enumerate(row):
                x_array.append(x)
                y_array.append(y)
                z_array.append(self.correlation_map.correlation_map[x, y])
        self.canvas.axes.plot_trisurf(x_array, y_array, z_array, linewidth=0.1, antialiased=True, cmap='magma')
        self.canvas.axes.set_title("Correlation map")
        self.main_layout.addWidget(self.canvas)
