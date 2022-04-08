from matplotlib.backends.backend_qt import NavigationToolbar2QT
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QVBoxLayout, QWidget


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class ImageWidget(QWidget):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.canvas = self.__set_canvas()
        self.main_layout = self.__set_main_layout()
        self.tool_bar = self.__set_toolbar()
        self.__set_image()

    def __set_canvas(self):
        return MplCanvas(width=5, height=4, dpi=100)

    def __set_main_layout(self) -> QVBoxLayout:
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        return main_layout

    def __set_toolbar(self) -> NavigationToolbar2QT:
        toolbar = NavigationToolbar2QT(self.canvas, self)
        self.main_layout.addWidget(toolbar)
        return toolbar

    def __set_image(self):
        self.canvas.axes.imshow(self.image)
        self.main_layout.addWidget(self.canvas)
