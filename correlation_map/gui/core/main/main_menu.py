from PyQt5.QtWidgets import QMenu, QMenuBar


class MainMenu(QMenuBar):
    def __init__(self):
        super().__init__()
        self.settings_menu = self.__set_settings_menu()
        self.author_menu = self.__set_author_menu()
        self.help_menu = self.__set_help_menu()

    def __set_settings_menu(self):
        settings_menu = QMenu("&Settings", self)
        self.addMenu(settings_menu)
        return settings_menu

    def __set_help_menu(self):
        help_menu = QMenu("&Help", self)
        self.addMenu(help_menu)
        return help_menu

    def __set_author_menu(self):
        author_menu = QMenu("&Author", self)
        self.addMenu(author_menu)
        return author_menu
