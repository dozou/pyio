# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

requires = {"yapsy",
            "pyqt5",
            "pyqtchart",
            "pandas",
            "matplotlib",
            "numpy",
            }


setup(
    name="pybration",
    packages=find_packages(),
    version="0.1.0",
    author="takemuralabs",
    author_email="",
    url="",
    install_requires=requires
)
