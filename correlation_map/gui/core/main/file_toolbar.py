import cv2
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QFileDialog, QPushButton, QToolBar

from core.images.image import Image, ImageTypes
from core.images.image_container import ImageContainer


class FileToolBar(QToolBar):
    def __init__(self):
        super().__init__()
        self.__set_load_source_image_action()
        self.__set_load_destination_image_action()
        self.__set_save_all_images_action()

    def _load_source_image(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        image_path, _ = dlg.getOpenFileName()
        image = Image(image_path, ImageTypes.SOURCE_IMAGE)
        ImageContainer.add(image)

    def _load_destination_image(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        image_path, _ = dlg.getOpenFileName()
        image = Image(image_path, ImageTypes.DESTINATION_IMAGE)
        ImageContainer.add(image)

    def __set_load_source_image_action(self):
        load_source_image_action = QAction(self)
        load_source_image_action.setText("&LoadSourceImage")
        load_source_image_action.setIcon(QIcon(":file-new.svg"))
        load_source_image_action.triggered.connect(self._load_source_image)
        self.addAction(load_source_image_action)

    def __set_load_destination_image_action(self):
        load_destination_image_action = QAction(self)
        load_destination_image_action.setText("&LoadDestinationImage")
        load_destination_image_action.setIcon(QIcon(":file-new.svg"))
        load_destination_image_action.triggered.connect(self._load_source_image)
        self.addAction(load_destination_image_action)

    def __set_save_all_images_action(self):
        save_all_images_action = QAction(self)
        save_all_images_action.setText("&SaveImages")
        save_all_images_action.setIcon(QIcon(":file-new.svg"))
        self.addAction(save_all_images_action)

    # def __set_actions(self):
    #     self.newAction = QAction(self)
    #     self.newAction.setText("&New")
    #     self.newAction.setIcon(QIcon(":file-new.svg"))
    #     self.openAction = QAction(QIcon(":file-open.svg"), "&Open...", self)
    #     self.saveAction = QAction(QIcon(":file-save.svg"), "&Save", self)
    #     self.exitAction = QAction("&Exit", self)
    #     self.addAction(self.newAction)
    #     self.addAction(self.openAction)
    #     self.addAction(self.saveAction)
