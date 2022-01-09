# -*- coding: utf-8 -*-

import os

from ._debug import typechecked


@typechecked
def load_coeffs(filename: str) -> list[float]:
    """
    Loads IGRF coefficients from file.

    Args:
        filename : file containing coefficients
    Returns:
        g and h, one by one
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
