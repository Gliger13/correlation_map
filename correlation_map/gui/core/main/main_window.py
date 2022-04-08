"""Module contains class for main windows"""
import cv2
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox, QHBoxLayout, QMainWindow, QVBoxLayout, \
    QWidget

from gui.core.main.execution_toolbar import ExecutionToolBar
from gui.core.main.file_toolbar import FileToolBar
from gui.core.main.image_widget import ImageWidget
from gui.core.main.main_menu import MainMenu


class MainWindow(QMainWindow):
    """Main window model"""

    def __init__(self):
        super().__init__()
        self.__set_main_window_properties()
        self.menu_bar = self.__set_menu_bar()
        self.file_toolbar = self.__set_file_tool_bar()
        self.execution_tool_bar = self.__set_execution_tool_bar()
        self.main_widget = self.__set_main_widget()
        self.main_layout = self.__set_main_layout()
        self.source_image_widget = self.__set_image_widget()
        self.destination_image_widget = self.__set_image_widget()

    def __set_main_window_properties(self):
        """
        Set different global main window properties

        Main window properties to set:
        - windows size = full screen
        """
        self.setWindowState(Qt.WindowMaximized)

    def __set_menu_bar(self) -> MainMenu:
        """
        Configure menu bar for main window and returns it

        :return: configured main menu bar
        """
        main_menu_bar = MainMenu()
        self.setMenuBar(main_menu_bar)
        return main_menu_bar

    def __set_file_tool_bar(self) -> FileToolBar:
        """
        Configure file toolbar for main window

        :return: configured file toolbar
        """
        file_toolbar = FileToolBar()
        self.addToolBar(file_toolbar)
        return file_toolbar

    def __set_execution_tool_bar(self) -> ExecutionToolBar:
        """
        Configure execution toolbar for main window

        :return: configured execution toolbar
        """
        execution_toolbar = ExecutionToolBar()
        self.addToolBar(execution_toolbar)
        return execution_toolbar

    def __set_main_widget(self) -> QWidget:
        """
        Configure main widget for main window

        :return: main widget
        """
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        return central_widget

    def __set_main_layout(self):
        """
        Configure main layout for main widget

        :return: main layout
        """
        main_layout = QHBoxLayout(self.main_widget)
        return main_layout

    def __set_image_widget(self) -> QWidget:
        image_layout = QVBoxLayout(self.main_widget)
        self.main_layout.addLayout(image_layout)

        image_chooser = QComboBox()
        image_layout.addWidget(image_chooser)

        img = cv2.imread("/home/andrei/Projects/Python/correlation_map/correlation_map/cat.jpg")
        image_widget = ImageWidget(img)
        image_layout.addWidget(image_widget)
        return image_widget
