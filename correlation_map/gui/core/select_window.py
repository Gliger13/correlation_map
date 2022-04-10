from PyQt5 import QtWidgets

from correlation_map.gui.windows import region


class DialogRegionSettings(QtWidgets.QDialog, region.Ui_Dialog):
    def __init__(self, user):
        super().__init__()
        self.current_user = user
        self.setupUi(self)
        self.setWindowTitle('Укажите область для сравнения')
        self.pushButton.clicked.connect(self.show_image)
        self.x1 = self.lineEdit.setText(str(self.current_user.x1))
        self.y1 = self.lineEdit_2.setText(str(self.current_user.y1))
        self.x2 = self.lineEdit_3.setText(str(self.current_user.x2))
        self.y2 = self.lineEdit_4.setText(str(self.current_user.y2))
        self.pushButton_2.clicked.connect(self.end_dialog)

    def end_dialog(self):
        self.save_corr_input()
        self.close()

    @staticmethod
    def is_correct_input(coordinate, line_edit):
        if not coordinate:
            line_edit.setStyleSheet("background-color: red;")
            return False
        else:
            try:
                int(coordinate)
            except ValueError:
                line_edit.setStyleSheet("background-color: red;")
                return False
        line_edit.setStyleSheet("background-color: lime;")
        return True

    def save_corr_input(self):
        self.x1 = self.lineEdit.text()
        self.y1 = self.lineEdit_2.text()
        self.x2 = self.lineEdit_3.text()
        self.y2 = self.lineEdit_4.text()
        if (self.is_correct_input(self.x1, self.lineEdit) and
                self.is_correct_input(self.y1, self.lineEdit_2) and
                self.is_correct_input(self.x2, self.lineEdit_3) and
                self.is_correct_input(self.y2, self.lineEdit_4)):
            self.current_user.x1 = int(self.x1)
            self.current_user.y1 = int(self.y1)
            self.current_user.x2 = int(self.x2)
            self.current_user.y2 = int(self.y2)
            return True
        return False

    def show_image(self):
        pass
        # if not self.current_user.image1_path:
        #     self.label.setText('Изображение на найдено!')
        #     self.label.setStyleSheet("background-color: red;")
        #     return
        # image = cv2.imread(self.current_user.image1_path)
        # if not self.save_corr_input():
        #     img_process.view_image("Input image", image)
        #     return
        # top_left = (self.current_user.x1, self.current_user.y1)
        # bottom_right = (self.current_user.x2, self.current_user.y2)
        # image = img_process.select_region(self.current_user.image1_path, top_left, bottom_right)
        # img_process.view_image("Selected region", image)
