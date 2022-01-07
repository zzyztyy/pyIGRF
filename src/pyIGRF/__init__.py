# -*- coding: utf-8 -*-

"""
`pyIGRF` is a Python package offering the IGRF-13 (International Geomagnetic Reference Field) model. You can use it to calculate the magnetic field's intensity and to transform coordinates between GeoGraphical and GeoMagnetic. The package does not require any Fortran compiler - it is pure Python.
"""

__author__ = 'pyIGRF authors'

from ._calculate import (
    geodetic2geocentric,
    get_syn,
)

from ._coeffs import (
    GH,
    get_coeffs,
    load_coeffs,
)

from ._value import (
    get_value,
    get_variation,
)
