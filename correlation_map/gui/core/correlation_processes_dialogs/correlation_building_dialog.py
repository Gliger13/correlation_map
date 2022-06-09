"""Module contains dialog wrapper for correlation building process"""
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLabel, QProgressBar, QPushButton, QVBoxLayout, QWidget

from correlation_map.core.config.correlation import CorrelationConfiguration
from correlation_map.core.correlation.correlation_map_pipeline_builder import CorrelationMapPipelineBuilder, \
    CorrelationStageAttributes
from correlation_map.gui.tools.common import log_configuration_process
from correlation_map.gui.tools.logger import app_logger


class CorrelationBuildingDialog(QDialog):
    """Dialog for start correlation building button and for correlation building information"""

    def __init__(self, correlation_configuration: CorrelationConfiguration):
        """
        :param correlation_configuration: filled correlation configuration to run building
        """
        super().__init__()
        self.correlation_configuration = correlation_configuration

        self.__configure_main_attributes()
        self._main_layout = self.__configure_main_layout()

        self.current_status_label = self.__configure_current_status_label()
        self.progress_bar = self.__configure_progress_bar()
        self.start_button = self.__configure_start_button()
        self.action_buttons = self.__configure_action_buttons()

    def start_correlation_process(self):
        """Start correlation map building

        Start correlation map building through stages. Update progress bar and text label after each completed stage.
        """
        app_logger.info("User clicked start correlation map building button")
        correlation_map_builder = CorrelationMapPipelineBuilder(self.correlation_configuration)
        for stage in correlation_map_builder.start_correlation_building_pipeline():
            self.progress_bar.setValue(stage.pipeline_progress)
            self.current_status_label.setText(stage.stage_attributes.message)
            self.update()
        app_logger.info("Correlation map built")

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
    def __configure_current_status_label(self) -> QLabel:
        """Configure and return current status label"""
        current_status_label_widget = QWidget()
        current_status_label = QLabel(current_status_label_widget)
        current_status_label.setText(CorrelationStageAttributes.START.message)
        self._main_layout.addWidget(current_status_label)
        return current_status_label

    @log_configuration_process
    def __configure_progress_bar(self) -> QProgressBar:
        """Configure and return progress bar"""
        progress_bar_widget = QWidget()
        progress_bar = QProgressBar(progress_bar_widget)
        self._main_layout.addWidget(progress_bar)
        return progress_bar

    def __configure_start_button(self) -> QPushButton:
        """Configure and return start correlation process button"""
        start_button_widget = QWidget()
        start_button = QPushButton("Start correlation map building", start_button_widget)
        start_button.pressed.connect(self.start_correlation_process)
        self._main_layout.addWidget(start_button)
        return start_button

    @log_configuration_process
    def __configure_action_buttons(self) -> QDialogButtonBox:
        """Configure and return dialog action buttons"""
        action_buttons_box = QDialogButtonBox(QDialogButtonBox.Cancel)
        action_buttons_box.accepted.connect(self.accept)
        action_buttons_box.rejected.connect(self.reject)
        self._main_layout.addWidget(action_buttons_box)
        return action_buttons_box
