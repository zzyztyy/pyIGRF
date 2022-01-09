# -*- coding: utf-8 -*-

import gc
import itertools
import os
from time import time_ns

import matplotlib.pyplot as plt

import numpy as np
from tqdm import tqdm
from typeguard import typechecked

from pyIGRF import get_syn


DTYPE = 'f4'
FLD = os.path.dirname(__file__)


@typechecked
def _single_run(
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

    years = [1910.0, 1940.0, 1980.0, 2000.0, 2020.0, 2025.0]
    iterations = [10 ** exp for exp in range(1, 5)]
    itypes = (1, 2)

    fig, ax = plt.subplots(figsize = (10, 10), dpi = 150)

    for year, itype in tqdm(itertools.product(years, itypes), total = len(years) * len(itypes)):

        durations = [
            _single_run(year = year, iterations = iteration, itype = itype) / iteration
            for iteration in iterations
        ]

        ax.loglog(
            iterations, durations, label = f'{year:.02f} | {itype:d}',
            linestyle = 'solid' if itype == 1 else 'dashed'
        )

    ax.legend()
    ax.set_xlabel('iterations')
    ax.set_ylabel('time per itertation [s]')
    ax.grid()

    fig.tight_layout()
    fig.savefig(os.path.join(FLD, 'benchmark_scalar_base.png'))


if __name__ == '__main__':
    main()
