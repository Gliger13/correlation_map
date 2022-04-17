"""Contains execution toolbar for the main window"""

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMessageBox, QToolBar

from correlation_map.core.config.correlation import PreprocessorActions
from correlation_map.core.config.variables import ProjectFileMapping
from correlation_map.core.images.image import ImageTypes
from correlation_map.core.images.image_container import ImageContainer
from correlation_map.gui.core.correlation_processes_dialogs.correlation_start_settings_dialog import \
    CorrelationStartSettingsDialog
from correlation_map.gui.core.correlation_processes_dialogs.important_part_chooser_dialog import \
    ImageImportantPartChooserDialog
from correlation_map.gui.tools.logger import app_logger
from correlation_map.gui.tools.path_factory import ProjectPathFactory


class ExecutionToolBar(QToolBar):
    """Execution toolbar for the main window"""

    def __init__(self):
        super().__init__()
        self.add_image_window_action = self.__set_add_image_window_action()
        self.run_action = self.__set_run_action()
        self.stop_action = self.__set_stop_action()
        self.terminate_action = self.__set_terminate_action()

    def check_for_loaded_source_and_destination_images(self) -> bool:
        """Check if user loaded source and destination images

        Check of user loaded source and destination images. If it's false, then call dialog with information.
        """
        if ImageContainer.is_contain_specific_image(ImageTypes.SOURCE_IMAGE) and \
                ImageContainer.is_contain_specific_image(ImageTypes.DESTINATION_IMAGE):
            return True
        if not ImageContainer.is_contain_specific_image(ImageTypes.SOURCE_IMAGE):
            dialog_message = "Not all images for correlation loaded. Please load source and destination images to " \
                             "build correlation map"
        elif not ImageContainer.is_contain_specific_image(ImageTypes.DESTINATION_IMAGE):
            dialog_message = "Not all images for correlation loaded. Please load destination image to build " \
                             "correlation map"
        else:
            dialog_message = "Not all images for correlation loaded. Please load source and destination images to " \
                             "build correlation map"

        QMessageBox.information(
            self,
            "Not all images loaded",
            dialog_message,
            buttons=QMessageBox.Ok,
            defaultButton=QMessageBox.Ok,
        )
        return False

    def start_correlation_map_building_process(self):
        """Start correlation map building process

        1) Allow user to select correlation configurations
        2) Allow user to choose image important part if he wants
        """
        app_logger.info("User configuring correlation configuration")
        if not self.check_for_loaded_source_and_destination_images():
            app_logger.info("User didn't load all needed images to build correlation map")
            return None

        correlation_start_dialog = CorrelationStartSettingsDialog()
        correlation_settings_dialog_exit_code = correlation_start_dialog.exec()
        if not correlation_settings_dialog_exit_code:
            app_logger.info("User canceled correlation configuration dialog")
            return None

        if correlation_start_dialog.preprocessor_checks_map[PreprocessorActions.CHOSE_IMPORTANT_PART].isChecked():
            app_logger.info("User choosing image important part")
            image_important_part_chooser_dialog = ImageImportantPartChooserDialog()
            part_chooser_dialog_exit_code = image_important_part_chooser_dialog.exec()
            if not part_chooser_dialog_exit_code:
                app_logger.info("User does not want to continue while choosing image important part")
                return None
        else:
            app_logger.info("User does not want to choose important image part for correlation")
        return None

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
