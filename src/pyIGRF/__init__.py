# -*- coding: utf-8 -*-

"""
`pyCRGI` is a Python package offering the IGRF-13 (International Geomagnetic Reference Field) model. You can use it to calculate the magnetic field's intensity and to transform coordinates between GeoGraphical and GeoMagnetic. The package does not require any Fortran compiler - it is pure Python.
"""

__author__ = 'pyCRGI authors'

from ._coeffs import (
    GH,
    load_coeffs,
)
