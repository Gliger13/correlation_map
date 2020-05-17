# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'region.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(324, 147)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 0, 301, 20))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 20, 301, 96))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 5)
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 0, 0, 1, 5)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_3.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout.addWidget(self.lineEdit_3, 3, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 3, 2, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 2, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_2.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 1, 3, 1, 2)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_4.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout.addWidget(self.lineEdit_4, 3, 3, 1, 2)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(10, 120, 141, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(169, 120, 141, 23))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Укажите область для сравнения"))
        self.label_2.setText(_translate("Dialog", "x1 = "))
        self.label_6.setText(_translate("Dialog", "Координаты нижней правой точки"))
        self.label_7.setText(_translate("Dialog", "Координаты верхней левой точки"))
        self.label_3.setText(_translate("Dialog", "x2 ="))
        self.label_5.setText(_translate("Dialog", "y2 = "))
        self.label_4.setText(_translate("Dialog", "y1 = "))
        self.pushButton.setText(_translate("Dialog", "показать область"))
        self.pushButton_2.setText(_translate("Dialog", "закрыть"))
