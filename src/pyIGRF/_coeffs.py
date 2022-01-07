# -*- coding: utf-8 -*-

import os
import warnings

from ._typeguard import typechecked


@typechecked
def load_coeffs(filename: str) -> list[float]:
    """
    load igrf12 coeffs from file
    :param filename: file which save coeffs (str)
    :return: g and h list one by one (list(float))
    """

    with open(filename, mode = 'r', encoding = 'utf-8') as f:
        gh2arr = [
            [float(coeff) for coeff in line.strip('\n').split()[3:]]
            for line in f
            if line.startswith('g ') or line.startswith('h ')
        ]

    gh2arr = list(map(list, zip(*gh2arr))) # transpose

    gh = []
    for idx, column in enumerate(gh2arr):
        stop = 120 if idx < 19 else None
        for coeff in column[:stop]:
            gh.append(coeff)
    gh.append(0)

    return gh


GH = load_coeffs(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'igrf13coeffs.txt'))


@typechecked
def get_coeffs(date: float) -> tuple[list, list]:
    """
    :param gh: list from load_coeffs
    :param date: float
    :return: list: g, list: h
    """

    if date < 1900.0 or date > 2030.0:
        warnings.warn((
            f"Will not work with a date of {date:f}. "
            "Date must be in the range 1900.0 <= date <= 2030.0. "
            "On return [], []"
        ), RuntimeWarning)
        return [], []
    elif date >= 2020.0:
        if date > 2025.0:
            warnings.warn((
                "This version of the IGRF is intended for use up to 2025.0."
                f"Values for {date:f} will be computed but may be of reduced accuracy."
            ), RuntimeWarning) # not adapt for the model but can calculate
        t = date - 2020.0
        tc = 1.0
        # pointer for last coefficient in pen-ultimate set of MF coefficients...
        ll = 3060 + 195
        nmx = 13
        nc = nmx * (nmx + 2)
    else:
        t = 0.2 * (date - 1900.0)
        ll = int(t)
        t = t - ll
        # SH models before 1995.0 are only to degree 10
        if date < 1995.0:
            nmx = 10
            nc = nmx * (nmx + 2)
            ll = nc * ll
        else:
            nmx = 13
            nc = nmx * (nmx + 2)
            ll = int(0.2 * (date - 1995.0))
            # 19 is the number of SH models that extend to degree 10
            ll = 120 * 19 + nc * ll
        tc = 1.0 - t

    g, h = [], []
    temp = ll - 1
    for n in range(nmx + 1):
        g.append([])
        h.append([])
        if n == 0:
            g[0].append(None)
        for m in range(n + 1):
            if m != 0:
                g[n].append(tc * GH[temp] + t * GH[temp + nc])
                h[n].append(tc * GH[temp + 1] + t * GH[temp + nc + 1])
                temp += 2
            else:
                g[n].append(tc * GH[temp] + t * GH[temp + nc])
                h[n].append(None)
                temp += 1

    return g, h
