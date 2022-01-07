# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


SRC_DIR = "src"


with open("README.md", mode = 'r', encoding = 'utf-8') as f:
    readme = f.read()


setup(
    name = "pyIGRF",
    version = "0.3.3",
    author = "pyIGRF authors",
    author_email = "ernst@pleiszenburg.de",
    description = "IGRF-13 Model by Python",
    long_description = readme,
    license = "MIT",
    url = "https://github.com/pleiszenburg/pyIGRF",
    packages = find_packages(SRC_DIR),
    package_dir = {"": SRC_DIR},
    install_requires = [],
    extras_require = {
        "dev": [
            "goto-statement",
            "typeguard",
        ]
    },
    package_data = {'': ['src/igrf13coeffs.txt']}
)
