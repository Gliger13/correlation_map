"""Contain scripts for paths"""
import os.path

PROJECT_ROOT_NAME = "correlation_map"


def get_abs_root_path(path: str) -> str:
    """
    Return absolute root path of the project

    :param path: Any file path of the project
    :return: Absolute root path of the project
    """
    root_dir = os.path.dirname(path)
    if os.path.basename(root_dir) == PROJECT_ROOT_NAME:
        return root_dir
    else:
        return get_abs_root_path(root_dir)


def get_abs_image_path(image_path: str) -> str:
    """
    Returns absolute path of a image

    :param image_path: Project image path
    :return: Absolute image path
    """
    root_path = get_abs_root_path(__file__)
    return os.path.join(root_path, image_path)
