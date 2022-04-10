"""Contains file toolbar model for main window"""

from PyQt5.QtWidgets import QAction, QFileDialog, QToolBar

from correlation_map.core.images.image import Image, ImageTypes
from correlation_map.core.images.image_container import ImageContainer
from correlation_map.gui.core.main.image_main_layout import ImageMainLayout
from correlation_map.gui.tools.logger import app_logger


class FileToolBar(QToolBar):
    """File toolbar model for main window"""

    __active_image_layouts: list[ImageMainLayout] = []

    def __init__(self):
        super().__init__()
        self.__set_load_source_image_action()
        self.__set_load_destination_image_action()
        self.__set_save_all_images_action()

    def add_image_layout(self, image_layout: ImageMainLayout):
        """Add image layout for support and maintain if there is a new image

        :param image_layout: image layout to maintain
        """
        self.__active_image_layouts.append(image_layout)

    @classmethod
    def _load_image(cls, image_type: ImageTypes):
        """Load image from file dialog

        - Show a file dialog and let the user choose an image
        - Wrapp chosen image and save it in the image's container
        - Update all image widgets and image choosers

        :param image_type: image type to load
        """
        app_logger.debug("User choosing `%s` image", image_type.value)
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        image_path, _ = file_dialog.getOpenFileName()

        if not image_path:
            app_logger.debug("User didn't choose `%s`", image_type.value)
            return

        app_logger.info("User chosen `%s` image with path `%s`", image_type.value, image_path)
        image = Image(image_path, image_type)
        ImageContainer.add(image)
        cls._update_widgets(image)

    @classmethod
    def _update_widgets(cls, new_image: Image):
        """Update all main image widgets and image choosers

        :param new_image: new loaded image wrapper
        """
        for image_layout in cls.__active_image_layouts:
            image_layout.image_chooser.update_items()
            if image_layout.image_widget.image.image_type == new_image.image_type:
                image_layout.set_image(force_update=True)

    def __set_load_source_image_action(self):
        """Set action on file toolbar to select and load new source image"""
        load_source_image_action = QAction(self)
        load_source_image_action.setText("&Load source image")
        load_source_image_action.triggered.connect(lambda: self._load_image(ImageTypes.SOURCE_IMAGE))
        self.addAction(load_source_image_action)
        app_logger.debug("Load source image action connected")

    def __set_load_destination_image_action(self):
        """Set action on file toolbar to select and load new destination image"""
        load_destination_image_action = QAction(self)
        load_destination_image_action.setText("&Load destination image")
        load_destination_image_action.triggered.connect(lambda: self._load_image(ImageTypes.DESTINATION_IMAGE))
        self.addAction(load_destination_image_action)
        app_logger.debug("Load destination image action connected")

    def __set_save_all_images_action(self):
        """Set action on file toolbar to save images"""
        save_all_images_action = QAction(self)
        save_all_images_action.setText("&Save images")
        self.addAction(save_all_images_action)
        app_logger.debug("Save all images action connected")
