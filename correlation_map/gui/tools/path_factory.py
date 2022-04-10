"""Contain factory to get different project paths"""
import os
from functools import lru_cache
from typing import Optional

from core.config.variables import ProjectFileMapping
from gui.tools.logger import app_loger


class ProjectPathFactory:
    """Provide different project paths"""

    @classmethod
    @lru_cache
    def get_root_dir_path(cls) -> str:
        """Gets abs path of the root project directory

        :raise AssertionError: when system root directory reached while searching for root project directory
        :return: absolute path to the root project directory
        """
        current_directory_path = os.path.dirname(__file__)
        while os.path.basename(current_directory_path) != ProjectFileMapping.ROOT_DIR_NAME:
            directory_path = os.path.dirname(current_directory_path)
            assert directory_path != current_directory_path, "System root directory reached while searching " \
                                                             "for root project directory"
            current_directory_path = directory_path
        return current_directory_path

    @classmethod
    @lru_cache
    def get_dir_path_in_project_by_name(cls, dir_name: str) -> Optional[str]:
        """Gets directory path in current project by it name

        :param dir_name: directory name in project files
        :return: directory path to the given directory in the project
        """
        for root_path, dirs, filenames in os.walk(cls.get_root_dir_path(), topdown=True):
            dirs[:] = [directory for directory in dirs if directory not in ProjectFileMapping.EXCLUDED_DIRS]
            if dir_name in dirs:
                return os.path.join(root_path, dir_name)
        app_loger.warning("Unable to get directory path in the project by directory name %s. Not found", dir_name)
        return None
