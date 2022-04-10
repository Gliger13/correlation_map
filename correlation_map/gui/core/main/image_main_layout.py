"""Contains vertical layout wrapper for all image widgets"""
from PyQt5.QtWidgets import QVBoxLayout, QWidget

from core.images.image import ImageTypes
from core.images.image_container import ImageContainer
from gui.core.main.image_chooser import ImageChooserComboBox
from gui.core.main.image_widget import ImageWidget
from gui.tools.logger import app_logger


class ImageMainLayout(QVBoxLayout):
    """Vertical layout for all image widgets"""

    def __init__(self, widget_to_attach: QWidget):
        """
        :param widget_to_attach: widget for attaching a layout
        """
        super().__init__(widget_to_attach)
        self.image_chooser = self.__configure_image_chooser()
        self.image_widget = self.__configure_default_image_widget()
        self.image_chooser.activated.connect(self.set_image)

    def __configure_image_chooser(self) -> ImageChooserComboBox:
        """Configure and return image chooser combo box"""
        image_chooser = ImageChooserComboBox()
        self.addWidget(image_chooser)
        app_logger.debug("Image chooser box configured")
        return image_chooser

    def __configure_default_image_widget(self) -> ImageWidget:
        """Configure and return image widget with default image"""
        image = ImageContainer.get(ImageTypes.DEFAULT_IMAGE)
        image_widget = ImageWidget(image)
        self.addWidget(image_widget)
        app_logger.debug("Image widget with default image has been set")
        return image_widget

    def set_image(self, force_update: bool = False):
        """Set new image widget by type from the image chooser box

        Get image type from the current image chooser combo box and get image wrapper from the image container using it.
        Replace the current image widget with a new widget with the image wrapper from the image container.

        :param force_update: if True then update the image widget even if it is of the same type as the current one
        """
        user_choice = self.image_chooser.currentText()
        app_logger.debug("User chosen `%s` in the image chooser", user_choice)
        chosen_image_type = ImageTypes.get_by_name(user_choice)
        if not chosen_image_type:
            app_logger.warning("Chosen wrong image type by image chooser box. Selected `%s`. Ignoring", user_choice)
            return None
        if not force_update and self.image_widget.image.image_type == chosen_image_type:
            app_logger.debug("The selected image with type `%s` is the same as the current one. Ignoring",
                             self.image_widget.image.image_type.value)
            return None
        app_logger.info("Setting image with type `%s`", chosen_image_type.value)
        image = ImageContainer.get(chosen_image_type)
        new_image_widget = ImageWidget(image)
        self.removeWidget(self.image_widget)
        self.addWidget(new_image_widget)
        self.image_widget = new_image_widget
        app_logger.info("Image with type `%s` was set", chosen_image_type.value)
        return None
