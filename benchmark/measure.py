#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gc
import itertools
import json
import os
from time import time_ns
from typing import Callable, Dict

import numpy as np
from tqdm import tqdm
from typeguard import typechecked

from pyCRGI.pure import get_syn as pure_get_syn
from pyCRGI.jited import get_syn as jited_get_syn
from pyCRGI.array import get_syn as array_get_syn


FLD = os.path.dirname(__file__)


@typechecked
def _single_run(
    get_syn: Callable,
    year: float,
    iterations: int,
    itype: int,
) -> float:

    offset = 0.0 if itype == 1 else 6371.2

    random = np.random.default_rng()

    lats = [float(number) for number in random.uniform(low = -90.0, high = 90.0, size = iterations)]
    lons = [float(number) for number in random.uniform(low = 0.0, high = 360.0, size = iterations)]
    alts = [float(number + offset) for number in random.uniform(low = -100.0, high = 400.0, size = iterations)]

    gc.disable()
    start = time_ns()

    for lat, lon, alt in zip(lats, lons, alts):

        _, _, _, _ = get_syn(
            year = year,
            lat = lat,
            elong = lon,
            alt = alt,
            itype = itype,
        )

    stop = time_ns()
    gc.enable()

    return (stop - start) * 1e-9


@typechecked
def _array_run(
    year: float,
    iterations: int,
    itype: int,
) -> float:

    offset = 0.0 if itype == 1 else 6371.2

    random = np.random.default_rng()

    lats = random.uniform(low = -90.0, high = 90.0, size = iterations).astype('f8')
    lons = random.uniform(low = 0.0, high = 360.0, size = iterations).astype('f8')
    alts = random.uniform(low = -100.0, high = 400.0, size = iterations).astype('f8') + offset

    gc.disable()
    start = time_ns()

    _ = array_get_syn(
        years = year,
        lats = lats,
        elongs = lons,
        alts = alts,
        itype = itype,
    )

    stop = time_ns()
    gc.enable()

    return (stop - start) * 1e-9


@typechecked
def _log(fn: str, data: Dict):
    with open(fn, mode = 'a', encoding='utf-8') as f:
        f.write(f'{json.dumps(data):s}\n')
        f.flush()


def main():

    _, _, _, _ = jited_get_syn(
        year = 1900.0,
        lat = 0.0,
        elong = 0.0,
        alt = 0.0,
        itype = 1,
    ) # jit warmup
    _ = array_get_syn(
        years = 1900.0,
        lats = np.array([0.0], dtype = 'f8'),
        elongs = np.array([0.0], dtype = 'f8'),
        alts = np.array([0.0], dtype = 'f8'),
        itype = 1,
    ) # jit warmup

    years = [1910.0, 1940.0, 1980.0, 2000.0, 2020.0, 2025.0]
    iterations = [10 ** exp for exp in range(1, 6)]
    itypes = (1, 2)
    funcs = (
        ('pure', pure_get_syn),
        ('jited', jited_get_syn),
    )

    shades = [
        idx / len(years)
        for idx in range(1, len(years) + 1)
    ][::-1]

    FN = os.path.join(FLD, 'data.txt')

    for (idx, year), itype, in tqdm(itertools.product(enumerate(years), itypes), total = len(years) * len(itypes)):

        for name, get_syn in funcs:

            durations = [
                _single_run(get_syn = get_syn, year = year, iterations = iteration, itype = itype) / iteration
                for iteration in iterations
            ]

            _log(FN, {
                'name': name,
                'year': year,
                'itype': itype,
                'iterations': iterations,
                'durations': durations,
                'color': [1, shades[idx], shades[idx], 1] if name == 'pure' else [shades[idx], 1, shades[idx], 1],
            })

        durations = [
            _array_run(year = year, iterations = iteration, itype = itype) / iteration
            for iteration in iterations
        ]

        _log(FN, {
            'name': 'array',
            'year': year,
            'itype': itype,
            'iterations': iterations,
            'durations': durations,
            'color': [shades[idx], shades[idx], 1, 1],
        })

if __name__ == '__main__':
    main()
