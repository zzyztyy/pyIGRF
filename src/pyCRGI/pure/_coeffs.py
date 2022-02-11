# -*- coding: utf-8 -*-

import warnings

from .._coeffs import GH
from .._debug import typechecked, DEBUG


@typechecked
def get_coeffs(year: float) -> tuple[list, list]:
    """
    Processes coefficients

    Args:
        year : Between 1900.0 and 2030.0
    Returns:
        g and h
    """

    if year < 1900.0 or year > 2030.0:
        if DEBUG:
            warnings.warn((
                f"Will not work with a date of {year:f}. "
                "Date must be in the range 1900.0 <= year <= 2030.0. "
                "On return [], []"
            ), RuntimeWarning)
        return [], []

    if year > 2025.0 and DEBUG:
        warnings.warn((
            "This version of the IGRF is intended for use up to 2025.0 ."
            f"Values for {year:f} will be computed but may be of reduced accuracy."
        ), RuntimeWarning) # not adapt for the model but can calculate

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

    g, h = [], []
    temp = ll - 1
    for n in range(nmx + 1):
        gsub = []
        hsub = []
        if n == 0:
            gsub.append(None)
        for m in range(n + 1):
            if m != 0:
                gsub.append(tc * GH[temp] + t * GH[temp + nc])
                hsub.append(tc * GH[temp + 1] + t * GH[temp + nc + 1])
                temp += 2
            else:
                gsub.append(tc * GH[temp] + t * GH[temp + nc])
                hsub.append(None)
                temp += 1
        g.append(gsub)
        h.append(hsub)

    return g, h
