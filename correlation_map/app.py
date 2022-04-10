"""Contains application main call function"""
import logging

from core.config.variables import check_required_environment_variables
from gui.manager import WindowsManager

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    check_required_environment_variables()
    windows_manager = WindowsManager()
    windows_manager.start_application()
