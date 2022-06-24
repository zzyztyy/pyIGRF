# -*- coding: utf-8 -*-

"""
JIT-compiled implementation, 2nd experimental edition
"""

from ._calculate import (
    geodetic2geocentric,
    get_syn,
)

from ._coeffs import (
    get_g_coeff,
    get_h_coeff,
    get_coeffs_prepare,
    GH,
)

from ._value import (
    get_value,
    get_variation,
)
