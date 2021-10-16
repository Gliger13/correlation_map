from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QToolBar


class FileToolBar(QToolBar):
    def __init__(self):
        super().__init__()
        self.__set_load_source_image_action()
        self.__set_load_destination_image_action()
        self.__set_save_all_images_action()

    def __set_load_source_image_action(self):
        load_source_image_action = QAction(self)
        load_source_image_action.setText("&LoadSourceImage")
        load_source_image_action.setIcon(QIcon(":file-new.svg"))
        self.addAction(load_source_image_action)

    def __set_load_destination_image_action(self):
        load_destination_image_action = QAction(self)
        load_destination_image_action.setText("&LoadDestinationImage")
        load_destination_image_action.setIcon(QIcon(":file-new.svg"))
        self.addAction(load_destination_image_action)

    def __set_save_all_images_action(self):
        save_all_images_action = QAction(self)
        save_all_images_action.setText("&SaveAllImages")
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
