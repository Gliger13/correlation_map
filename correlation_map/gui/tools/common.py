"""Contains common utils to work with PyQT"""
from PyQt5 import sip
from PyQt5.QtWidgets import QLayout


def delete_layout(layout: QLayout):
    """Delete PyQT layout

    :param layout: layout to delete
    """
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.deleteLater()
        else:
            delete_layout(item.layout())
    sip.delete(layout)
