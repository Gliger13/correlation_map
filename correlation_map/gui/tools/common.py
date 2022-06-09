"""Contains common utils to work with PyQT"""
from functools import wraps
from typing import Callable

from PyQt5 import sip
from PyQt5.QtWidgets import QLayout

from correlation_map.gui.tools.logger import tools_logger


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


def log_configuration_process(configuration_method: Callable) -> Callable:
    """Log before and after UI QT thing configuration

    :param configuration_method: method to wrapp with debug logs
    """
    @wraps(configuration_method)
    def wrapper(*args, **kwargs):
        configuration_name = configuration_method.__name__.replace("_", " ").lstrip().capitalize()
        configuration_method_module = configuration_method.__module__.split(".")[-1]
        tools_logger.debug("%s: Start %s", configuration_method_module, configuration_name)
        result = configuration_method(*args, **kwargs)
        tools_logger.debug("%s: End %s", configuration_method_module, configuration_name)
        return result
    return wrapper
