# -*- coding: utf-8 -*-

"""
JIT-compiled implementation, 2nd experimental edition
"""

from ._calculate import (
    geodetic2geocentric,
    get_syn,
)

from ._coeffs import (
    get_coeffs,
    GH,
)

from ._value import (
    get_value,
    get_variation,
)
