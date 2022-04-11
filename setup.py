"""Module to set up correlation map package"""
from os.path import dirname, join

from setuptools import find_packages, setup

# Package meta-data
PROJECT_NAME = 'correlation_map'
PROJECT_VERSION = '1.0.0'
DESCRIPTION = "Create correlation maps of two images with PyQT GUI"
AUTHOR = "Andrei Zaneuski"
AUTHOR_EMAIL = "zanevskiyandrey@gmail.com"
URL = "https://github.com/Gliger13/correlation_map"
LONG_DESCRIPTION = open(join(dirname(__file__), 'README.md'), "utf-8").read()

TESTS_ADDITIONAL_REQUIREMENTS = [
    "pytest"
]

setup(
    name=PROJECT_NAME,
    version=PROJECT_VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    long_description=LONG_DESCRIPTION,
    package_dir={"correlation_map": "correlation_map"},
    packages=find_packages(),
    install_requires=open(join(dirname(__file__), 'requirements.txt'), "utf-8").read(),
    package_data={"correlation_map": ['gui/static/*']},
    scripts=['correlation_map/app.py'],
    tests_require=TESTS_ADDITIONAL_REQUIREMENTS,
)
