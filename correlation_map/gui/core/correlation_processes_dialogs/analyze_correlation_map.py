"""Analyze correlation map dialog

Module contains dialog wrapper for analyzing correlation maps."""
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLabel, QSpinBox, QVBoxLayout, QWidget

from correlation_map.gui.tools.common import log_configuration_process


class CorrelationMapAnalyzerDialog(QDialog):
    """Dialog for analyzing correlation map"""

    def __init__(self):
        super().__init__()
        self.__configure_main_attributes()
        self._main_layout = self.__configure_main_layout()

        self.settings_label = self.__configure_description_label()
        self.search_limit_sping_box = self.__configure_search_limit()
        self.action_button_box = self.__configure_action_buttons()

    def __configure_main_attributes(self):
        """Configure dialog main attributes"""
        self.setWindowTitle("Correlation building process")

    @log_configuration_process
    def __configure_main_layout(self) -> QVBoxLayout:
        """Configure and return main layout for the dialog"""
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        return main_layout

    @log_configuration_process
    def __configure_description_label(self):
        correlation_settings_label_widget = QWidget()
        correlation_settings_label = QLabel(correlation_settings_label_widget)
        correlation_settings_label.setText("Correlation map analysis settings:")
        self._main_layout.addWidget(correlation_settings_label)
        return correlation_settings_label

    @log_configuration_process
    def __configure_search_limit(self):
        search_limit_spin_box = QSpinBox()
        search_limit_spin_box.setValue(80)
        search_limit_spin_box.setRange(0, 100)
        self._main_layout.addWidget(search_limit_spin_box)
        return search_limit_spin_box

    @log_configuration_process
    def __configure_action_buttons(self) -> QDialogButtonBox:
        """Configure and return dialog action buttons"""
        action_buttons_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        action_buttons_box.accepted.connect(self.accept)
        action_buttons_box.rejected.connect(self.reject)
        self._main_layout.addWidget(action_buttons_box)
        return action_buttons_box
