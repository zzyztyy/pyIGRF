# -*- coding: utf-8 -*-

import numba as nb
import numpy as np

from .._coeffs import GH
from .._debug import typechecked


GH = np.array(GH, dtype = 'f8')
SH = 13 # maximum number of spherical harmonics


@nb.njit('i8(f8,f8[:,:,:])')
def _get_coeff(year, gh):
    """
    Processes coefficients

    Args:
        year : Between 1900.0 and 2030.0
        gh : g and h (output)
    Returns:
        Width/height of g and h
    """

    if year < 1900.0 or year > 2030.0:
        return 0

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

    return nmx + 1


@nb.njit('(f8[:],f8[:,:,:,:],f8[:])', parallel = True)
def get_coeffs(years, ghs, shs):
    """
    Processes coefficients

    Args:
        years : Array of years between 1900.0 and 2030.0
        ghs : Array of g and h (output)
        shs : Array of number of spherical harmonics plus one (output)
    """

    assert years.shape[0] == ghs.shape[0] == shs.shape[0]
    assert ghs.shape[1] == 2
    assert ghs.shape[2] == SH + 1 and ghs.shape[3] == SH + 1

    for idx in nb.prange(years.shape[0]):

        shs[idx] = _get_coeff(years[idx], ghs[idx, ...])


@typechecked
def malloc_coeffs(years: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Allocate memory

    Args:
        years : Array of years between 1900.0 and 2030.0
    Returns:
        ghs: Array of g and h (output); shs: Array of number of spherical harmonics plus one (output)
    """

    assert years.ndim == 1
    assert years.dtype == np.float64

    ghs = np.zeros((years.shape[0], 2, SH + 1, SH + 1), dtype = 'f8')
    shs = np.zeros((years.shape[0],), dtype = 'f8')

    return ghs, shs
