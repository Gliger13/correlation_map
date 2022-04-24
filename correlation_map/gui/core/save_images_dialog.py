"""Contains save images dialog model"""
import os
from typing import Optional

from PyQt5.QtWidgets import QCheckBox, QDialog, QDialogButtonBox, QFileDialog, QHBoxLayout, QLabel, QPushButton, \
    QVBoxLayout, QWidget

from correlation_map.core.config.figure_types import FigureType
from correlation_map.core.models.figures.figure_container import FigureContainer
from correlation_map.gui.tools.common import log_configuration_process
from correlation_map.gui.tools.logger import app_logger


class SaveImagesDialog(QDialog):
    """QDialog wrapper to save user images from the image container"""

    def __init__(self):
        app_logger.debug("Initializing save images dialog")
        super().__init__()
        self.images_path_to_save = os.getcwd()

        self._main_layout = self.__configure_main_layout()
        if FigureContainer.is_contains_user_images():
            self.image_chooser_layout = self.__configure_image_chooser_layout()
            self.image_path_label = self.__configure_image_path_label()
            self.image_choose_button = self.__configure_image_choose_button()
            self.dialog_action_buttons = QDialogButtonBox.Save | QDialogButtonBox.Cancel
            self.image_chooser_check_boxes = self.__configure_image_chooser_boxes()
        else:
            self.dialog_action_buttons = QDialogButtonBox.Close
            self.nothing_to_save_label = self.__configure_nothing_to_save_label()
        self.__configure_attributes()
        self.actions_buttons_box = self.__configure_action_buttons_box()
        app_logger.debug("Save images dialog initialized")

    def choose_path_to_save(self) -> Optional[str]:
        """Open file dialog and allow user to choose directory path to save images

        :return: directory path to save images
        """
        app_logger.info("User choosing path to save images")
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.Directory)
        file_dialog.setOption(QFileDialog.ShowDirsOnly)
        image_path = file_dialog.getExistingDirectory()

        if not image_path:
            app_logger.debug("User doesn't choose path")
            return None
        app_logger.info("User chosen pat `%s` to save images", image_path)
        self.images_path_to_save = image_path
        self.image_path_label.setText(self.images_path_to_save)
        return image_path

    def get_images_to_save(self) -> list[FigureType]:
        """Return images types to save from the checkboxes that user checked

        :return: list of image types that user checked
        """
        return [FigureType.get_by_name(check_box.text()) for check_box in self.image_chooser_check_boxes
                if check_box.isChecked()]

    @log_configuration_process
    def __configure_attributes(self):
        """Configure global dialog attributes"""
        self.setWindowTitle("Save images")

    @log_configuration_process
    def __configure_main_layout(self) -> QVBoxLayout:
        """Configure and return main layout for the dialog"""
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        return main_layout

    @log_configuration_process
    def __configure_nothing_to_save_label(self) -> QLabel:
        """Configure and return save label"""
        label_widget = QWidget()
        label = QLabel(label_widget)
        label.setText("No images to save")
        self._main_layout.addWidget(label)
        return label

    @log_configuration_process
    def __configure_image_chooser_layout(self) -> QHBoxLayout:
        """Configure and return image chooser layout for label and directory chooser button"""
        image_path_chooser_layout = QHBoxLayout()
        self._main_layout.addLayout(image_path_chooser_layout)
        return image_path_chooser_layout

    @log_configuration_process
    def __configure_image_path_label(self) -> QLabel:
        """Configure and return image label with path to directory to save images"""
        image_path_label_widget = QWidget()
        image_path_label = QLabel(image_path_label_widget)
        image_path_label.setText(self.images_path_to_save)
        self.image_chooser_layout.addWidget(image_path_label)
        return image_path_label

    @log_configuration_process
    def __configure_image_choose_button(self) -> QPushButton:
        """Configure and return button to select path to directory to save images"""
        image_chooser_button_widget = QWidget()
        image_chooser_button = QPushButton(image_chooser_button_widget)
        image_chooser_button.pressed.connect(self.choose_path_to_save)
        image_chooser_button.setText("Choose path")
        self.image_chooser_layout.addWidget(image_chooser_button)
        return image_chooser_button

    @log_configuration_process
    def __configure_image_chooser_boxes(self) -> list[QCheckBox]:
        """Configure and return list of checkboxes with image types to save"""
        to_save_label_widget = QWidget()
        to_save_label = QLabel(to_save_label_widget)
        to_save_label.setText("To save:")
        self._main_layout.addWidget(to_save_label)

        check_boxes: list[QCheckBox] = []
        for image_to_choose in FigureContainer.get_all_user_images():
            check_box = QCheckBox(image_to_choose.figure_type.value.capitalize())
            check_box.setChecked(True)
            self._main_layout.addWidget(check_box)
            check_boxes.append(check_box)
        return check_boxes

    @log_configuration_process
    def __configure_action_buttons_box(self):
        """Configure box with actions buttons"""
        action_buttons_box = QDialogButtonBox(self.dialog_action_buttons)
        action_buttons_box.accepted.connect(self.accept)
        action_buttons_box.rejected.connect(self.reject)
        self._main_layout.addWidget(action_buttons_box)
        return action_buttons_box
