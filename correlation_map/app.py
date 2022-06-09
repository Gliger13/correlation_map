#! /usr/local/bin/python3
# -*- coding: utf-8 -*-

"""Contains application main enter point"""
from correlation_map.core.config.config_check import check_required_environment_variables
from correlation_map.gui.manager import WindowsManager
from correlation_map.gui.tools.logger import app_logger

if __name__ == '__main__':
    app_logger.debug("Starting correlation map application")
    check_required_environment_variables()
    windows_manager = WindowsManager()
    windows_manager.start_application()
