# -*- coding: utf-8 -*-

import gc
import itertools
import os
from time import time_ns
from typing import Callable

import matplotlib.pyplot as plt

import numpy as np
from tqdm import tqdm
from typeguard import typechecked

from pyIGRF.pure import get_syn as pure_get_syn
from pyIGRF.jited import get_syn as jited_get_syn


DTYPE = 'f4'
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
    alts = [float(number) for number in random.uniform(low = -100.0, high = 400.0, size = iterations)]

    gc.disable()
    start = time_ns()

    for lat, lon, alt in zip(lats, lons, alts):

        _, _, _, _ = get_syn(
            year = year,
            lat = lat,
            elong = lon,
            alt = alt + offset,
            itype = itype,
        )

    stop = time_ns()
    gc.enable()

    return (stop - start) * 1e-9


def main():

    _, _, _, _ = jited_get_syn(
        year = 1900.0,
        lat = 0.0,
        elong = 0.0,
        alt = 0.0,
        itype = 1,
    ) # jit warmup

    years = [1910.0, 1940.0, 1980.0, 2000.0, 2020.0, 2025.0]
    iterations = [10 ** exp for exp in range(1, 5)]
    itypes = (1, 2)
    funcs = (
        ('pure', pure_get_syn),
        ('jited', jited_get_syn),
    )

    fig, ax = plt.subplots(figsize = (10, 10), dpi = 150)

    for year, itype, (name, get_syn) in tqdm(itertools.product(
        years, itypes, funcs,
    ), total = len(years) * len(itypes) * len(funcs)):

        durations = [
            _single_run(get_syn = get_syn, year = year, iterations = iteration, itype = itype) / iteration
            for iteration in iterations
        ]

        ax.loglog(
            iterations, durations, label = f'{name:s} | {year:.02f} | {itype:d}',
            linestyle = 'solid' if itype == 1 else 'dashed'
        )

    ax.legend()
    ax.set_xlabel('iterations')
    ax.set_ylabel('time per itertation [s]')
    ax.grid()

    fig.tight_layout()
    fig.savefig(os.path.join(FLD, 'benchmark_scalar.png'))


if __name__ == '__main__':
    main()
