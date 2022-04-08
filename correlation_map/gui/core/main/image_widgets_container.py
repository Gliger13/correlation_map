from gui.core.main.image_widget import ImageWidget


class ImageWidgetsContainer:
    __image_widgets = []

    def add(self, widget: ImageWidget):
        self.__image_widgets.append(widget)