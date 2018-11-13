#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function
from setuptools import setup, find_packages


setup(
    name="pyIGRF",
    version="0.1.8",
    author="zzyztyy",
    author_email="2375672032@qq.com",
    description="IGRF-12 Model by Python",
    long_description=open("README.md").read(),
    license="MIT",
    url="https://github.com/zzyztyy/pyIGRF",
    packages=find_packages(),
    install_requires=[
        "NumPy"
    ],
    package_data={'': ['src/igrf12coeffs.txt']}
)
