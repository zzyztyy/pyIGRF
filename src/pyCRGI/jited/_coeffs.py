# -*- coding: utf-8 -*-

import numba as nb
import numpy as np

from .._coeffs import GH


GH = np.array(GH, dtype = 'f8')


@nb.njit('f8[:,:,:](f8)')
def get_coeffs(year):
    """
    Processes coefficients

    Args:
        year : Between 1900.0 and 2030.0
    Returns:
        g and h
    """

    if year < 1900.0 or year > 2030.0:
        return np.zeros((
            2, # g/h
            0,
            0,
        ), dtype = 'f8')

    if year >= 2020.0:
        t = year - 2020.0
        tc = 1.0
        # pointer for last coefficient in pen-ultimate set of MF coefficients...
        ll = 3060 + 195
        nmx = 13
        nc = nmx * (nmx + 2)
    else:
        t = 0.2 * (year - 1900.0)
        ll = int(t)
        t = t - ll
        # SH models before 1995.0 are only to degree 10
        if year < 1995.0:
            nmx = 10
            nc = nmx * (nmx + 2)
            ll = nc * ll
        else:
            nmx = 13
            nc = nmx * (nmx + 2)
            ll = int(0.2 * (year - 1995.0))
            # 19 is the number of SH models that extend to degree 10
            ll = 120 * 19 + nc * ll
        tc = 1.0 - t

    # Moving forward: nmx, ll, t, tc, nc

    gh = np.zeros((
        2, # g/h
        nmx + 1,
        nmx + 1,
    ), dtype = 'f8')

    temp = ll - 1
    for n in range(nmx + 1):
        if n == 0:
            gh[0, n, 0] = np.nan
            offset = 1
        else:
            offset = 0
        for m in range(n + 1):
            if m != 0:
                gh[0, n, m+offset] = tc * GH[temp] + t * GH[temp + nc]
                gh[1, n, m] = tc * GH[temp + 1] + t * GH[temp + nc + 1]
                temp += 2
            else:
                gh[0, n, m+offset] = tc * GH[temp] + t * GH[temp + nc]
                gh[1, n, m] = np.nan
                temp += 1

    return gh
