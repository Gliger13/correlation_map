from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QToolBar


class ExecutionToolBar(QToolBar):
    def __init__(self):
        super().__init__()
        self.__set_run_action()
        self.__set_stop_action()
        self.__set_terminate_action()

    def __set_run_action(self):
        run_action = QAction(self)
        run_action.setText("&Run")
        run_action.setIcon(QIcon(":file-new.svg"))
        self.addAction(run_action)

    def __set_stop_action(self):
        stop_action = QAction(self)
        stop_action.setText("&Stop")
        stop_action.setIcon(QIcon(":file-new.svg"))
        self.addAction(stop_action)

    def __set_terminate_action(self):
        terminate_action = QAction(self)
        terminate_action.setText("&Terminate")
        terminate_action.setIcon(QIcon(":file-new.svg"))
        self.addAction(terminate_action)
