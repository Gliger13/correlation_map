"""Contains dialog wrapper to configure correlation map building"""
from typing import Dict

from PyQt5.QtWidgets import QCheckBox, QDialog, QDialogButtonBox, QHBoxLayout, QLabel, QRadioButton, QSpinBox, \
    QVBoxLayout, QWidget

from correlation_map.core.config.correlation import CorrelationConfiguration, CorrelationSettings, CorrelationTypes, \
    PreprocessorActions
from correlation_map.gui.tools.common import log_configuration_process
from correlation_map.gui.tools.logger import app_logger


class CorrelationStartSettingsDialog(QDialog):
    """Dialog wrapper to configure correlation map building"""

    def __init__(self):
        super().__init__()
        self.__configure_main_attributes()
        self._main_layout = self.__configure_main_layout()

        self.preprocessor_checks_map = self.__configure_preprocessor_action_check_boxes()
        self.correlation_radio_buttons_map = self.__configure_correlation_type_radio_buttons()
        self.correlation_settings_map = self.__configure_correlation_settings_spin_boxes()
        self.action_buttons = self.__configure_action_buttons()

    def update_correlation_configuration(self, correlation_configuration: CorrelationConfiguration) \
            -> CorrelationConfiguration:
        """Update correlation configuration with the user input from the current dialog widgets

        :param correlation_configuration: correlation configuration wrapper to update
        :return: update correlation configuration with the data from the dialog input widgets
        """
        # Updating preprocessor configurations
        auto_rotation_check_box = self.preprocessor_checks_map[PreprocessorActions.AUTO_ROTATION]
        correlation_configuration.auto_rotate = auto_rotation_check_box.isChecked()
        auto_find_check_box = self.preprocessor_checks_map[PreprocessorActions.AUTO_FIND]
        correlation_configuration.auto_find = auto_find_check_box.isChecked()
        chose_important_part = self.preprocessor_checks_map[PreprocessorActions.CHOSE_IMPORTANT_PART]
        correlation_configuration.chose_important_part = chose_important_part.isChecked()
        # Updating correlation type
        correlation_configuration.correlation_type = self.get_checked_correlation_type()
        # Updating correlation settings
        detection_match_count_widget = self.correlation_settings_map[CorrelationSettings.DETECTION_MATCH_COUNT]
        correlation_configuration.detection_match_count = detection_match_count_widget.value()
        correlation_pieces_count_widget = self.correlation_settings_map[CorrelationSettings.CORRELATION_PIECES_COUNT]
        correlation_configuration.correlation_pieces_count = correlation_pieces_count_widget.value()
        return correlation_configuration

    def get_checked_correlation_type(self) -> CorrelationTypes:
        """Get checked correlation type from the all correlation type radio buttons

        :return: checked correlation type
        """
        for correlation_type, radio_button in self.correlation_radio_buttons_map.items():
            if radio_button.isChecked():
                return correlation_type
        app_logger.warning("Impossible design error. Checked correlation type not found. Using default one")
        return next(correlation for correlation in CorrelationTypes if correlation.is_default)

    def __configure_main_attributes(self):
        """Configure dialog main attributes"""
        self.setWindowTitle("Correlation build settings")

    @log_configuration_process
    def __configure_main_layout(self) -> QVBoxLayout:
        """Configure and return main layout for the dialog"""
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        return main_layout

    @log_configuration_process
    def __configure_preprocessor_action_check_boxes(self) -> Dict[PreprocessorActions, QCheckBox]:
        """Configure preprocessor action check boxes

        :return: map of preprocessor action name and check box widget items
        """
        preprocessor_description_label_widget = QWidget()
        preprocessor_description_label = QLabel(preprocessor_description_label_widget)
        preprocessor_description_label.setText("Preprocessor actions:")
        self._main_layout.addWidget(preprocessor_description_label)
        preprocessor_checks_map: dict[PreprocessorActions, QCheckBox] = {}
        for action in PreprocessorActions:
            check_box = QCheckBox(action.value.capitalize())
            check_box.setChecked(True)
            self._main_layout.addWidget(check_box)
            preprocessor_checks_map[action] = check_box
        return preprocessor_checks_map

    @log_configuration_process
    def __configure_correlation_type_radio_buttons(self) -> Dict[CorrelationTypes, QRadioButton]:
        """Configure correlation type radio buttons

        :return: map of correlation type name and radio button widget items
        """
        correlation_types_label_widget = QWidget()
        correlation_types_label = QLabel(correlation_types_label_widget)
        correlation_types_label.setText("Correlation type:")
        self._main_layout.addWidget(correlation_types_label)
        correlation_radio_buttons_map: dict[CorrelationTypes, QRadioButton] = {}
        for correlation_type in CorrelationTypes:
            radio_button = QRadioButton(correlation_type.correlation_type.replace("_", " ").capitalize())
            if correlation_type.is_default:
                radio_button.setChecked(True)
            self._main_layout.addWidget(radio_button)
            correlation_radio_buttons_map[correlation_type] = radio_button
        return correlation_radio_buttons_map

    @log_configuration_process
    def __configure_correlation_settings_spin_boxes(self) -> dict[CorrelationSettings, QSpinBox]:
        """Configure correlation settings spin boxes

        :return: map of correlation setting name and spin box widget items
        """
        correlation_settings_label_widget = QWidget()
        correlation_settings_label = QLabel(correlation_settings_label_widget)
        correlation_settings_label.setText("Correlation settings:")
        self._main_layout.addWidget(correlation_settings_label)
        correlation_settings_widgets_map: dict[CorrelationSettings, QSpinBox] = {}
        for correlation_setting in CorrelationSettings:
            horizontal_layout = QHBoxLayout()
            description_label_widget = QWidget()
            description_label = QLabel(description_label_widget)
            description_label.setText(correlation_setting.setting.capitalize())
            horizontal_layout.addWidget(description_label)
            spin_box = QSpinBox()
            spin_box.setValue(correlation_setting.default_value)
            horizontal_layout.addWidget(spin_box)
            correlation_settings_widgets_map[correlation_setting] = spin_box
            self._main_layout.addLayout(horizontal_layout)
        return correlation_settings_widgets_map

    @log_configuration_process
    def __configure_action_buttons(self) -> QDialogButtonBox:
        """Configure and return dialog action buttons"""
        action_buttons_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        action_buttons_box.accepted.connect(self.accept)
        action_buttons_box.rejected.connect(self.reject)
        self._main_layout.addWidget(action_buttons_box)
        return action_buttons_box
