"""Contains main menu model"""
from PyQt5.QtWidgets import QMenu, QMenuBar


class MainMenu(QMenuBar):
    """Main menu bar for main application window"""

    def __init__(self):
        super().__init__()
        self.author_menu = self.__set_author_menu()

    def __set_author_menu(self):
        """Set author menu"""
        author_menu = QMenu("&Author", self)
        self.addMenu(author_menu)
        return author_menu
