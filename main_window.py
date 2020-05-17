import os
import sys

import cv2
from PyQt5 import QtWidgets

import correlation_process
import img_process
import select_window
import author_window
from gui_forms import main_window


class MainWindow(QtWidgets.QMainWindow, main_window.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        self.user = UserActions()
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.setWindowTitle('Параметры обработки изображений')
        self.action_author.triggered.connect(self.show_author)
        # Start calculation
        self.pushButton.clicked.connect(self.start_calculations)
        # Settings of setting region of image1
        self.toolButton_3.clicked.connect(self.region_settings)
        # Chose path of image1
        self.toolButton.clicked.connect(self.chose_file_2)
        # Chose path of image2
        self.toolButton_2.clicked.connect(self.chose_file_3)
        # Set default type of correlation
        self.radioButton.setChecked(True)
        # Set default value for progress bar
        self.progressBar.setValue(0)

    def update_progress(self, name):
        self.progressBar.setValue(self.user.progress)
        self.label_10.setText("Прогресс: " + name)
        self.user.progress += 1

    @staticmethod
    def show_author():
        author_dialog = author_window.DialogAuthor()
        author_dialog.show()
        author_dialog.exec_()

    def region_settings(self):
        region_dialog = select_window.DialogRegionSettings(self.user)
        region_dialog.show()
        region_dialog.exec_()

    def _calculation(self):
        image1 = cv2.imread(self.user.image1_path)
        image2 = cv2.imread(self.user.image2_path)

        if self.user.show_src:
            self.update_progress("показ исходного изображения")
            cv2.imshow("Source image", image1)
        if self.user.show_new:
            self.update_progress("показ нового изображения")
            cv2.imshow("New image", image2)

        if self.user.flag_autorotate:
            lines_count = int(self.spinBox.text())
            self.update_progress("нахождение угла поворота")
            theta = img_process.find_theta(image1, image2, is_show=self.user.show_detected, lines=lines_count)
            self.update_progress("переворот нового изображения")
            image2 = img_process.rotate_img(image2, theta)
            if self.user.show_new_rot:
                self.update_progress("показ повернутого изображения")
                cv2.imshow("Rotated new image", image2)

        if self.user.flag_select:
            if not (not self.user.x1 or not self.user.y1 or
                    not self.user.x2 or not self.user.y2):
                top_left = self.user.x1, self.user.y1
                bottom_right = self.user.x2, self.user.y2
                self.update_progress("обрезка исходного изображения")
                image1 = img_process.get_image_zone(image1, top_left, bottom_right)
                if self.user.show_src_sel:
                    self.update_progress("показ обрезанной части")
                    cv2.imshow("Selected region on new image", image2)

        if self.user.flag_find:
            self.update_progress("поиск исх. в новом")
            image2_found, image2 = correlation_process.find_and_cut(image2, image1, self.user.correlation)
            if self.user.show_new_find:
                self.update_progress("показ найденной области")
                cv2.imshow("Image with region found by correlation", image2_found)
            if self.user.show_new_sel:
                self.update_progress("показ найденной области")
                cv2.imshow("Region that found by correlation", image2)

        if self.user.show_correlation_map:
            delim = int(self.spinBox_2.text())
            self.update_progress("начало построение карты")
            result_map = correlation_process.corr_map(image1, image2, delim, self.user.correlation)
            self.user.progress = 99 - self.user.progress
            self.update_progress("загрузка результатов в виде графика")
            correlation_process.view_map(result_map)

    def start_calculations(self):
        self.user.progress = 0
        self.update_progress('начало обработки')
        if not self.textBrowser_1.toPlainText():
            self.textBrowser_1.setStyleSheet("background-color: red;")
            return
        else:
            self.textBrowser_1.setStyleSheet("background-color: lime;")
        if not self.textBrowser_2.toPlainText():
            self.textBrowser_2.setStyleSheet("background-color: red;")
            return
        else:
            self.textBrowser_2.setStyleSheet("background-color: lime;")

        if self.checkBox.isChecked():
            self.user.flag_autorotate = True
        if self.checkBox_2.isChecked():
            self.user.flag_select = True
        if self.checkBox_3.isChecked():
            self.user.show_src = True
        if self.checkBox_4.isChecked():
            self.user.show_src_sel = True
        if self.checkBox_10.isChecked():
            self.user.show_new = True
        if self.checkBox_5.isChecked():
            self.user.show_new_rot = True
        if self.checkBox_6.isChecked():
            self.user.flag_find = True
        if self.checkBox_7.isChecked():
            self.user.show_new_sel = True
        if self.checkBox_8.isChecked():
            self.user.show_new_find = True
        if self.checkBox_11.isChecked():
            self.user.show_detected = True
        if self.checkBox_9.isChecked():
            self.user.show_correlation_map = True
        if self.radioButton.isChecked():
            self.user.correlation = "TM_SQDIFF"
        if self.radioButton_2.isChecked():
            self.user.correlation = "TM_SQDIFF_NORMED"
        if self.radioButton_3.isChecked():
            self.user.correlation = "TM_CCORR"
        if self.radioButton_4.isChecked():
            self.user.correlation = "TM_CCORR_NORMED"
        if self.radioButton_5.isChecked():
            self.user.correlation = "TM_CCOEFF"
        if self.radioButton_6.isChecked():
            self.user.correlation = "TM_CCOEFF_NORMED"
        self._calculation()
        self.user.progress = 100
        self.update_progress("обработка закончена")

    def chose_file_2(self):
        # self.listWidget.clear()  # На случай, если в списке уже есть элементы
        image_path = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите исходное изображение")[0]
        self.textBrowser_1.append(os.path.basename(image_path))  # Засунуть в текстовый блок
        self.user.image1_path = image_path

    def chose_file_3(self):
        # self.listWidget.clear()  # На случай, если в списке уже есть элементы
        image_path = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите новое изображение")[0]
        self.textBrowser_2.append(os.path.basename(image_path))  # Засунуть в текстовый блок
        self.user.image2_path = image_path


class UserActions:
    def __init__(self):
        self.progress = 0
        self.image1_path = None
        # Select region of image1
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None

        self.image2_path = None
        # Type of correlation
        self.correlation = None
        # Image process
        self.flag_autorotate = False
        self.flag_select = False
        self.flag_find = False
        # Images to show
        self.show_src = False
        self.show_src_sel = False
        self.show_new = False
        self.show_new_rot = False
        self.show_new_find = False
        self.show_new_sel = False
        self.show_detected = False
        self.show_correlation_map = False


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
