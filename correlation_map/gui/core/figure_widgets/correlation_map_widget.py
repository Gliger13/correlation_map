"""Module contains widget for correlation map 3d plot"""
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from correlation_map.core.models.figures.correlation_map import CorrelationMap
from correlation_map.gui.core.figure_widgets.base_figure_widget import BaseFigureWidget


class Mpl3dCanvas(FigureCanvasQTAgg):
    """Figure canvas class inheritance to display image as 3d plot"""

    def __init__(self, width: int = 5, height: int = 4, dpi: int = 100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111, projection='3d')
        super().__init__(fig)


class CorrelationMapWidget(BaseFigureWidget):
    """Image widget wrapper for displaying an image as plot and plot tools"""

    def __init__(self, correlation_map: CorrelationMap):
        """
        :param correlation_map: correlation map to attach to the widget
        """
        super().__init__(correlation_map)

    def _get_canvas(self) -> FigureCanvasQTAgg:
        return Mpl3dCanvas(width=5, height=4, dpi=100)
