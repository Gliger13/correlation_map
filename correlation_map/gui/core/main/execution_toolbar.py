from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QToolBar

from core.config.variables import ProjectFileMapping
from gui.tools.path_factory import ProjectPathFactory


class ExecutionToolBar(QToolBar):
    def __init__(self):
        super().__init__()
        self.__set_run_action()
        self.__set_stop_action()
        self.__set_terminate_action()

    def __set_run_action(self):
        run_action = QAction(self)
        run_action.setText("&Run")
        run_icon = QIcon(ProjectPathFactory.get_static_file_path(ProjectFileMapping.RUN_ICON_FILE_NAME))
        run_action.setIcon(run_icon)
        self.addAction(run_action)

    def __set_stop_action(self):
        stop_action = QAction(self)
        stop_action.setText("&Stop")
        stop_icon = QIcon(ProjectPathFactory.get_static_file_path(ProjectFileMapping.STOP_ICON_FILE_NAME))
        stop_action.setIcon(stop_icon)
        self.addAction(stop_action)

    def __set_terminate_action(self):
        terminate_action = QAction(self)
        terminate_action.setText("&Terminate")
        terminate_icon = QIcon(ProjectPathFactory.get_static_file_path(ProjectFileMapping.TERMINATE_ICON_FILE_NAME))
        terminate_action.setIcon(terminate_icon)
        self.addAction(terminate_action)
