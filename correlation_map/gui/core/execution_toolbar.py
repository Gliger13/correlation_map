"""Contains execution toolbar for the main window"""

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QToolBar

from correlation_map.core.config.variables import ProjectFileMapping
from correlation_map.gui.core.correlation_processes_dialogs.correlation_start_settings_dialog import \
    CorrelationStartSettingsDialog
from correlation_map.gui.tools.path_factory import ProjectPathFactory


class ExecutionToolBar(QToolBar):
    """Execution toolbar for the main window"""

    def __init__(self):
        super().__init__()
        self.add_image_window_action = self.__set_add_image_window_action()
        self.run_action = self.__set_run_action()
        self.stop_action = self.__set_stop_action()
        self.terminate_action = self.__set_terminate_action()

    def start_correlation_map_building_process(self):
        """Start correlation map building process

        1) Allow user to select configurations
        """
        correlation_start_dialog = CorrelationStartSettingsDialog()
        correlation_start_dialog.exec()

    def __set_add_image_window_action(self):
        """Configure and return run correlation process action"""
        add_image_window_action = QAction(self)
        add_image_window_action.setText("&Add image window")
        icon = QIcon(ProjectPathFactory.get_static_file_path(ProjectFileMapping.ADD_IMAGE_WINDOW_ICON_FILE_NAME))
        add_image_window_action.setIcon(icon)
        self.addAction(add_image_window_action)
        return add_image_window_action

    def __set_run_action(self):
        """Configure and return run correlation process action"""
        run_action = QAction(self)
        run_action.setText("&Run")
        run_icon = QIcon(ProjectPathFactory.get_static_file_path(ProjectFileMapping.RUN_ICON_FILE_NAME))
        run_action.triggered.connect(self.start_correlation_map_building_process)
        run_action.setIcon(run_icon)
        self.addAction(run_action)
        return run_action

    def __set_stop_action(self):
        """Configure and return stop correlation process action"""
        stop_action = QAction(self)
        stop_action.setText("&Stop")
        stop_icon = QIcon(ProjectPathFactory.get_static_file_path(ProjectFileMapping.STOP_ICON_FILE_NAME))
        stop_action.setIcon(stop_icon)
        self.addAction(stop_action)
        return stop_action

    def __set_terminate_action(self):
        """Configure and return terminate correlation process action"""
        terminate_action = QAction(self)
        terminate_action.setText("&Terminate")
        terminate_icon = QIcon(ProjectPathFactory.get_static_file_path(ProjectFileMapping.TERMINATE_ICON_FILE_NAME))
        terminate_action.setIcon(terminate_icon)
        self.addAction(terminate_action)
        return terminate_action
