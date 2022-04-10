"""Contains main window's manager that controls main gui application and cycle"""
import logging
import sys
from traceback import format_exception

from PyQt5.uic.properties import QtWidgets

from gui.core.main.main_window import MainWindow


class WindowsManager:
    """Manager to control main application and cycle"""

    def __init__(self):
        self.__configure_exception_hook()
        self.application = QtWidgets.QApplication(sys.argv)
        self.main_window = MainWindow()

    def start_application(self):
        """Start main cycle and show main window"""
        self.main_window.show()
        self.application.exec_()

    @staticmethod
    def __configure_exception_hook():
        """Configure custom exception hook to debug PyQT5"""
        def except_hook(exc_type, exc_value, exc_tb):
            """For debug PyQT5 projects"""
            trace_back = "".join(format_exception(exc_type, exc_value, exc_tb))
            logging.critical("Critical error cached: %s", trace_back)
            QtWidgets.QApplication.quit()

        sys.excepthook = except_hook
