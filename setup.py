#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function
from setuptools import setup, find_packages

SRC_DIR = "src"

setup(
    name="pyIGRF",
    version="0.3.3",
    author="zzyztyy",
    author_email="2375672032@qq.com",
    description="IGRF-13 Model by Python",
    long_description=open("README.md").read(),
    license="MIT",
    url="https://github.com/zzyztyy/pyIGRF",
    packages=find_packages(SRC_DIR),
    package_dir={"": SRC_DIR},
    install_requires=[
        "NumPy"
    ],
    extras_require={
        "dev": [
            "goto-statement"
        ]
    },
    package_data={'': ['src/igrf13coeffs.txt']}
)
