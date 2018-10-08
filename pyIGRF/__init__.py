#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'zzyztyy'

"""
This is a package of IGRF-12 (International Geomagnetic Reference Field) about python version.
It don't need any Fortran compiler.
"""

from pyIGRF.value import igrf_variation, igrf_value
from pyIGRF import loadCoeffs, calculate
