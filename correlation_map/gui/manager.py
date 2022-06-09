"""Contains main window's manager that controls main gui application and cycle"""
import sys
from traceback import format_exception

from PyQt5 import QtWidgets

from correlation_map.gui.core.main_window import MainWindow
from correlation_map.gui.tools.logger import app_logger


class WindowsManager:
    """Manager to control main application and cycle"""

    def __init__(self):
        app_logger.debug("Starting windows manager")
        self.__configure_exception_hook()
        self.application = QtWidgets.QApplication(sys.argv)
        self.main_window = MainWindow()

    def start_application(self):
        """Start main cycle and show main window"""
        app_logger.debug("Starting main cycle and main window")
        self.main_window.show()
        app_logger.debug("Application initialized")
        self.application.exec_()

    @staticmethod
    def __configure_exception_hook():
        """Configure custom exception hook to debug PyQT5"""

        def except_hook(exc_type, exc_value, exc_tb):
            """For debug PyQT5 projects"""
            trace_back = "".join(format_exception(exc_type, exc_value, exc_tb))
            app_logger.critical("Critical error cached: %s", trace_back)
            QtWidgets.QApplication.quit()

        sys.excepthook = except_hook
