from PyQt5 import QtWidgets

from correlation_map.gui.windows import author


class DialogAuthor(QtWidgets.QDialog, author.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Автор')
