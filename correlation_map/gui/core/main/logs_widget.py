from PyQt5.QtWidgets import QFrame, QPlainTextEdit


class LogsWidget(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.__set_logs_widget()

    def __set_logs_widget(self):
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet('background-color:gray')
