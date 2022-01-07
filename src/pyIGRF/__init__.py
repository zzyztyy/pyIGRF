# -*- coding: utf-8 -*-

__author__ = 'zzyztyy'

"""
This is a package of IGRF-12 (International Geomagnetic Reference Field) about python version.
It don't need any Fortran compiler.
"""

from ._calculate import (
    geodetic2geocentric,
    igrf12syn,
)

from ._loadcoeffs import (
    GH,
    get_coeffs,
    load_coeffs,
)

from ._value import (
    get_value,
    get_variation,
)
