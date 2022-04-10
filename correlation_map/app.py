"""Contains application main call function"""

from core.config.config_check import check_required_environment_variables
from gui.manager import WindowsManager
from gui.tools.logger import app_logger

if __name__ == '__main__':
    app_logger.debug("Starting correlation map application")
    check_required_environment_variables()
    windows_manager = WindowsManager()
    windows_manager.start_application()
