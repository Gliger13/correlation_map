from PyQt5.QtWidgets import QApplication


class WindowsConfig:
    def __init__(self, app: QApplication):
        self.__app = app

    @property
    def desktop_size(self):
        return self.__app.desktop().size()
