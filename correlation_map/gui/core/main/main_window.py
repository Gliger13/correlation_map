from typing import Literal, Tuple

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QComboBox, QGridLayout, QHBoxLayout, QLabel, QMainWindow, QMenuBar, QSplitter, QVBoxLayout, \
    QWidget

from gui.core.main.execution_toolbar import ExecutionToolBar
from gui.core.main.image_widget import ImageWidget
from gui.core.main.logs_widget import LogsWidget
from gui.core.main.main_menu import MainMenu
from gui.core.main.file_toolbar import FileToolBar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__set_main_window_properties()
        self.menu_bar = self.__set_menu_bar()
        self.file_toolbar = self.__set_file_tool_bar()
        self.execution_tool_bar = self.__set_execution_tool_bar()
        self.main_widget = self.__set_main_widget()
        self.main_layout = self.__set_main_layout()
        self.image_layout = self.__set_image_layout()
        self.source_image_widget = self.__set_image_widget()
        self.destination_image_widget = self.__set_image_widget()
        # self.logs_widget = self.__set_logs_widget()

    def __set_menu_bar(self) -> QMenuBar:
        main_menu_bar = MainMenu()
        self.setMenuBar(main_menu_bar)
        return main_menu_bar

    def __set_file_tool_bar(self):
        file_toolbar = FileToolBar()
        self.addToolBar(file_toolbar)
        return file_toolbar

    def __set_execution_tool_bar(self):
        execution_toolbar = ExecutionToolBar()
        self.addToolBar(execution_toolbar)
        return execution_toolbar

    def __set_main_widget(self) -> QWidget:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        return central_widget

    def __set_main_layout(self):
        main_layout = QVBoxLayout(self.main_widget)
        return main_layout

    def __set_image_layout(self):
        image_layout = QHBoxLayout(self.main_widget)
        self.main_layout.addLayout(image_layout)
        return image_layout

    def __set_image_widget(self) -> QWidget:
        image_widget = ImageWidget()
        self.image_layout.addWidget(image_widget)
        image_part_layout = QVBoxLayout()
        self.image_layout.addLayout(QVBoxLayout())
        image_chooser = QComboBox()
        image_part_layout.addWidget(image_chooser)
        # image = QLabel().setPixmap(QPixmap("img.png"))
        # image_part_layout.addWidget(image)

        return image_widget

    def __set_main_window_properties(self):
        self.setWindowState(Qt.WindowMaximized)
    #
    # def __set_logs_widget(self):
    #     logs_widget = LogsWidget()
    #     self.main_layout.addWidget(logs_widget)
    #     return logs_widget
