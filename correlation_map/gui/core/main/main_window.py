"""Module contains class for main windows"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QMainWindow, QWidget

from core.config.variables import ProjectFileMapping
from core.images.image import Image, ImageTypes
from core.images.image_container import ImageContainer
from gui.core.main.execution_toolbar import ExecutionToolBar
from gui.core.main.file_toolbar import FileToolBar
from gui.core.main.image_main_layout import ImageMainLayout
from gui.core.main.main_menu import MainMenu
from gui.tools.logger import app_logger
from gui.tools.path_factory import ProjectPathFactory


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
        self.__add_default_image_to_image_container()
        self.active_image_layouts: list[ImageMainLayout] = [
            self.__set_image_main_layout(), self.__set_image_main_layout()
        ]

    def __set_main_window_properties(self):
        """Set different global main window properties

        Main window properties to set:
        - windows size = full screen
        """
        self.setWindowState(Qt.WindowMaximized)
        app_logger.debug("Main windows maximized")

    def __set_menu_bar(self) -> MainMenu:
        """Configure menu bar for main window and return it

        :return: configured main menu bar
        """
        main_menu_bar = MainMenu()
        self.setMenuBar(main_menu_bar)
        app_logger.debug("Main menubar configured")
        return main_menu_bar

    def __set_file_tool_bar(self) -> FileToolBar:
        """Configure file toolbar for main window

        :return: configured file toolbar
        """
        file_toolbar = FileToolBar()
        self.addToolBar(file_toolbar)
        app_logger.debug("File toolbar configured")
        return file_toolbar

    def __set_execution_tool_bar(self) -> ExecutionToolBar:
        """Configure execution toolbar for main window

        :return: configured execution toolbar
        """
        execution_toolbar = ExecutionToolBar()
        self.addToolBar(execution_toolbar)
        app_logger.debug("Execution toolbar configured")
        return execution_toolbar

    def __set_main_widget(self) -> QWidget:
        """Configure main widget for main window

        :return: main widget
        """
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        return central_widget

    def __set_main_layout(self):
        """Configure main layout for main widget

        :return: main layout
        """
        main_layout = QHBoxLayout(self.main_widget)
        return main_layout

    @classmethod
    def __add_default_image_to_image_container(cls):
        """Add default image to image container"""
        app_logger.debug("Loading and adding default image to image container")
        path_to_default_image = ProjectPathFactory.get_static_file_path(ProjectFileMapping.DEFAULT_IMAGE_NAME)
        default_image = Image(path_to_default_image, ImageTypes.DEFAULT_IMAGE)
        ImageContainer.add(default_image)
        app_logger.debug("Default image added to image container")

    def __set_image_main_layout(self) -> ImageMainLayout:
        """Configure and return image widget"""
        app_logger.debug("Configuring image main layout and it's widgets")
        image_main_layout = ImageMainLayout(self.main_widget)
        self.main_layout.addLayout(image_main_layout)
        self.file_toolbar.add_image_layout(image_main_layout)
        app_logger.debug("Image main layout and it's widgets configured")
        return image_main_layout
