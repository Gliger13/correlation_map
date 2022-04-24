"""Contains image widget class"""

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from correlation_map.core.models.figures.image import ImageWrapper
from correlation_map.gui.core.figure_widgets.base_figure_widget import BaseFigureWidget


class MplCanvas(FigureCanvasQTAgg):
    """Figure canvas class inheritance to display image as plot"""

    def __init__(self, width: int = 5, height: int = 4, dpi: int = 100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)


class ImageWidget(BaseFigureWidget):
    """Image widget wrapper for displaying an image as plot and plot tools"""

    def __init__(self, image: ImageWrapper):
        """
        :param image: image wrapper to attach to widget
        """
        super().__init__(image)
        self.figure = image

    def _get_canvas(self) -> FigureCanvasQTAgg:
        return MplCanvas(width=5, height=4, dpi=100)
