import logging
import os
import sys
import traceback

from PyQt5 import QtWidgets

from correlation_map.core.correlation.correlation_map_process_builder import CorrelationMapProcessBuilder
from correlation_map.core.user.user import UserActions
from correlation_map.gui.core import select_window, author_window
from correlation_map.gui.core.main.main_window import MainWindow
from correlation_map.gui.tools.windows_config import WindowsConfig
from correlation_map.gui.windows import main_window


# class MainWindow(QtWidgets.QMainWindow, main_window.Ui_MainWindow):
#     def __init__(self):
#         self.user = UserActions()
#         super().__init__()
#         self.setupUi(self)
#         self.setWindowTitle('Параметры обработки изображений')
#         self.action_author.triggered.connect(self.show_author)
#         # Start calculation
#         self.pushButton.clicked.connect(self.start_calculations)
#         # Settings of setting region of image1
#         self.toolButton_3.clicked.connect(self.region_settings)
#         # Chose path of image1
#         self.toolButton.clicked.connect(self.chose_file_2)
#         # Chose path of image2
#         self.toolButton_2.clicked.connect(self.chose_file_3)
#         # Set default type of correlation
#         self.radioButton.setChecked(True)
#         # Set default value for progress bar
#         self.progressBar.setValue(0)
#
#     def update_progress(self, name):
#         self.progressBar.setValue(self.user.progress)
#         self.label_10.setText("Прогресс: " + name)
#         self.user.progress += 1
#
#     @staticmethod
#     def show_author():
#         author_dialog = author_window.DialogAuthor()
#         author_dialog.show()
#         author_dialog.exec_()
#
#     def region_settings(self):
#         region_dialog = select_window.DialogRegionSettings(self.user)
#         region_dialog.show()
#         region_dialog.exec_()
#
#     def _calculation(self):
#         process = CorrelationMapProcessBuilder(self.user)
#         correlation_map = process.build_correlation_map()
#         correlation_map.view_correlation_map()
#
#     # def _calculation(self):
#     #     images_to_show = []
#     #     image_titles = []
#     #     image1 = cv2.imread(self.user.image1_path)
#     #     image2 = cv2.imread(self.user.image2_path)
#     #     logging.debug('Loaded images')
#     #     if not image1.any():
#     #         self.show_error("Не удалось загрузить исходное изображение")
#     #         return
#     #     if not image2.any():
#     #         self.show_error("Не удалось загрузить новое изображение")
#     #         return
#     #     if self.user.show_src:
#     #         images_to_show.append(image1)
#     #         image_titles.append("Исходное изображение")
#     #     if self.user.show_new:
#     #         images_to_show.append(image2)
#     #         image_titles.append("Новое изображение")
#     #
#     #     if self.user.flag_autorotate:
#     #         lines_count = int(self.spinBox.text())
#     #         self.update_progress("нахождение угла поворота")
#     #         theta, detected_img = img_process.find_theta(image1, image2, lines=lines_count)
#     #         logging.debug('Angle found')
#     #         self.update_progress("переворот нового изображения")
#     #         image2 = img_process.rotate_img(image2, theta)
#     #         logging.debug('Image rotated')
#     #         if self.user.show_detected:
#     #             images_to_show.append(detected_img)
#     #             image_titles.append("Процесс нахождения угла")
#     #         if self.user.show_new_rot:
#     #             images_to_show.append(image2)
#     #             image_titles.append("Повернутое новое относительно исходного")
#     #
#     #     if self.user.flag_select:
#     #         if self.user.x1 and self.user.y1 and self.user.x2 and self.user.y2:
#     #             top_left = self.user.x1, self.user.y1
#     #             bottom_right = self.user.x2, self.user.y2
#     #             self.update_progress("обрезка исходного изображения")
#     #             if self.user.show_src_sel:
#     #                 image = img_process.select_region(self.user.image1_path, top_left, bottom_right)
#     #                 images_to_show.append(image)
#     #                 image_titles.append("Выбранная область на исходном")
#     #             image1 = img_process.get_image_zone(image1, top_left, bottom_right)
#     #             logging.debug('Image cut')
#     #             if self.user.show_src_sel:
#     #                 images_to_show.append(image1)
#     #                 image_titles.append("Обрезанная область исходного")
#     #
#     #     if self.user.flag_find:
#     #         self.update_progress("поиск исх. в новом")
#     #         if image1.shape[0] <= image2.shape[0] and image1.shape[1] <= image2.shape[1]:
#     #             image2_found, image2 = correlation_process.find_and_cut(image2, image1, self.user.correlation)
#     #             logging.debug('Part of source was found')
#     #             if self.user.show_new_find:
#     #                 images_to_show.append(image2_found)
#     #                 image_titles.append("Найденная область благодаря корреляции")
#     #             if self.user.show_new_sel:
#     #                 images_to_show.append(image2)
#     #                 image_titles.append("Обрезанная найденная область благодаря корреляции")
#     #         else:
#     #             self.show_error('Поиск невозможен. Первое изображение больше второго.')
#     #             return
#     #
#     #     if self.user.show_correlation_map:
#     #         delim = int(self.spinBox_2.text())
#     #         self.update_progress("начало построение карты")
#     #         logging.debug('Correlation map: start process')
#     #         result_map = correlation_process.corr_map(image1, image2, delim, self.user.correlation)
#     #         logging.debug('Correlation map: end process')
#     #         self.user.progress = 99 - self.user.progress
#     #         self.update_progress("загрузка результатов в виде графика")
#     #         correlation_process.view_map(result_map)
#     #         logging.debug('Correlation map showed')
#     #     self.user.progress = 100
#     #     img_process.show_images(images_to_show, image_titles)
#
#     def show_error(self, text):
#         self.label.setText(text)
#         self.label.setStyleSheet('color: red;')
#
#     def start_calculations(self):
#         self.label.setText('Параметры обработки изображения')
#         self.label.setStyleSheet('color: black;')
#         self.user.progress = 0
#         self.update_progress('начало обработки')
#         if not self.textBrowser_1.toPlainText():
#             self.textBrowser_1.setStyleSheet("background-color: red;")
#             return
#         else:
#             self.textBrowser_1.setStyleSheet("background-color: lime;")
#         if not self.textBrowser_2.toPlainText():
#             self.textBrowser_2.setStyleSheet("background-color: red;")
#             return
#         else:
#             self.textBrowser_2.setStyleSheet("background-color: lime;")
#
#         if self.checkBox.isChecked():
#             self.user.flag_autorotate = True
#         if self.checkBox_2.isChecked():
#             self.user.flag_select = True
#         if self.checkBox_3.isChecked():
#             self.user.show_src = True
#         if self.checkBox_4.isChecked():
#             self.user.show_src_sel = True
#         if self.checkBox_10.isChecked():
#             self.user.show_new = True
#         if self.checkBox_5.isChecked():
#             self.user.show_new_rot = True
#         if self.checkBox_6.isChecked():
#             self.user.flag_find = True
#         if self.checkBox_7.isChecked():
#             self.user.show_new_sel = True
#         if self.checkBox_8.isChecked():
#             self.user.show_new_find = True
#         if self.checkBox_11.isChecked():
#             self.user.show_detected = True
#         if self.checkBox_9.isChecked():
#             self.user.show_correlation_map = True
#         if self.radioButton.isChecked():
#             self.user.correlation = "TM_SQDIFF"
#         if self.radioButton_2.isChecked():
#             self.user.correlation = "TM_SQDIFF_NORMED"
#         if self.radioButton_3.isChecked():
#             self.user.correlation = "TM_CCORR"
#         if self.radioButton_4.isChecked():
#             self.user.correlation = "TM_CCORR_NORMED"
#         if self.radioButton_5.isChecked():
#             self.user.correlation = "TM_CCOEFF"
#         if self.radioButton_6.isChecked():
#             self.user.correlation = "TM_CCOEFF_NORMED"
#         self._calculation()
#         self.user.progress = 100
#         self.update_progress("обработка закончена")
#         self.user.reset_choices()
#
#     def chose_file_2(self):
#         self.textBrowser_1.clear()
#         image_path = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите исходное изображение")[0]
#         self.textBrowser_1.append(os.path.basename(image_path))  # Засунуть в текстовый блок
#         self.user.image1_path = image_path
#
#     def chose_file_3(self):
#         self.textBrowser_2.clear()
#         image_path = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите новое изображение")[0]
#         self.textBrowser_2.append(os.path.basename(image_path))  # Засунуть в текстовый блок
#         self.user.image2_path = image_path


# def main():
#     sys.excepthook = excepthook
#     app = QtWidgets.QApplication(sys.argv)
#     config = WindowsConfig(app)
#     window = MainWindow()
#     window.show()
#     app.exec_()
#
#
# def excepthook(exc_type, exc_value, exc_tb):
#     """For debug PyQT5 projects"""
#     tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
#     print("error catched!:", tb)
#     QtWidgets.QApplication.quit()
