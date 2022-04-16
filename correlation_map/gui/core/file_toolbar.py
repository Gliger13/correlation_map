"""Contains file toolbar model for main window"""

from PIL import UnidentifiedImageError
from PyQt5.QtWidgets import QAction, QFileDialog, QToolBar

from correlation_map.core.images.image import ImageTypes, ImageWrapper
from correlation_map.core.images.image_container import ImageContainer
from correlation_map.gui.core.image_main_layout import ImageMainLayout
from correlation_map.gui.core.save_images_dialog import SaveImagesDialog
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

    def remove_image_layout(self, image_layout: ImageMainLayout):
        """Remove image main layout

        :param image_layout: image layout to remove
        """
        self.__active_image_layouts.remove(image_layout)

    @staticmethod
    def save_images():
        """Save all user chosen images in the user chosen directory path"""
        save_images_dialog = SaveImagesDialog()
        app_logger.info("User in the save images dialog. Waiting for the actions")
        user_choice = save_images_dialog.exec()
        if not user_choice:
            app_logger.debug("User doesn't want to save images. Exit dialog")
            return

        app_logger.info("User chosen to save `%s` images",
                        {image_type.value for image_type in save_images_dialog.get_images_to_save()})
        for image_type_to_save in save_images_dialog.get_images_to_save():
            for image in ImageContainer.get_all_user_images():
                if image.image_type == image_type_to_save:
                    image.save(save_images_dialog.images_path_to_save)
        app_logger.info("All selected images saved")

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

        try:
            image = ImageWrapper(image_path, image_type)
        except UnidentifiedImageError as error:
            app_logger.error("Cannot load file by path %s. Error: %s", image_path, error)
            return

        ImageContainer.add(image)
        cls._update_widgets(image)

    @classmethod
    def _update_widgets(cls, new_image: ImageWrapper):
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
        save_all_images_action.triggered.connect(self.save_images)
        self.addAction(save_all_images_action)
        app_logger.debug("Save all images action connected")
