"""Contains main menu model"""
from PyQt5.QtWidgets import QMenu, QMenuBar


class MainMenu(QMenuBar):
    """Main menu bar for main application window"""

    def __init__(self):
        super().__init__()
        self.settings_menu = self.__set_settings_menu()
        self.author_menu = self.__set_author_menu()
        self.help_menu = self.__set_help_menu()

    def __set_settings_menu(self):
        """Set setting menu"""
        settings_menu = QMenu("&Settings", self)
        self.addMenu(settings_menu)
        return settings_menu

    def __set_help_menu(self):
        """Set help menu"""
        help_menu = QMenu("&Help", self)
        self.addMenu(help_menu)
        return help_menu

    def __set_author_menu(self):
        """Set author menu"""
        author_menu = QMenu("&Author", self)
        self.addMenu(author_menu)
        return author_menu
