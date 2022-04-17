"""Module contains dialog wrapper to chose important part of the image"""
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout

from correlation_map.core.images.image import ImageTypes
from correlation_map.core.images.image_container import ImageContainer
from correlation_map.gui.core.image_widget import ImageWidget, ImageWidgetWithSelector
from correlation_map.gui.tools.common import log_configuration_process


class ImageImportantPartChooserDialog(QDialog):
    """Dialog wrapper to chose important part of the image"""

    def __init__(self):
        super().__init__()
        self.__configure_main_attributes()
        self._main_layout = self.__configure_main_layout()
        self.image_canvas = self.__configure_image_canvas()
        self.action_buttons_box = self.__configure_action_buttons()

    def __configure_main_attributes(self):
        """Configure dialog main attributes"""
        self.setWindowTitle("Choosing image important part")

    @log_configuration_process
    def __configure_main_layout(self) -> QVBoxLayout:
        """Configure and return main layout for the dialog"""
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        return main_layout

    @log_configuration_process
    def __configure_image_canvas(self) -> ImageWidget:
        image_widget = ImageWidgetWithSelector(ImageContainer.get(ImageTypes.SOURCE_IMAGE))
        self._main_layout.addWidget(image_widget)
        return image_widget

    @log_configuration_process
    def __configure_action_buttons(self):
        """Configure and return dialog action buttons"""
        action_buttons_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        action_buttons_box.accepted.connect(self.accept)
        action_buttons_box.rejected.connect(self.reject)
        self._main_layout.addWidget(action_buttons_box)
        return action_buttons_box
