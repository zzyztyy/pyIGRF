# -*- coding: utf-8 -*-

import gc
import itertools
from time import time_ns

import numpy as np
from tqdm import tqdm
from typeguard import typechecked

from pyIGRF import get_syn


DTYPE = 'f4'


@typechecked
def main(
    year_step: float = 0.5, # 0.5 ... 2.0
    lat_step: float = 7.5, # 7.5 ... 90.0
    lon_step: float = 7.5, # 7.5 ... 90.0
    alt_step: float = 49.5, # 49.5 ... 100.0
):

    years = np.arange(1900.0, 2030.0 + year_step, year_step, dtype = DTYPE)
    lats = np.arange(-90.0, 90.0 + lat_step, lat_step, dtype = DTYPE)
    lons = np.arange(0.0, 360.0, lon_step, dtype = DTYPE)
    alts = np.arange(-100.0, 400.0 + alt_step, alt_step, dtype = DTYPE)
    itypes = (1, 2) # above sea level, from centre of Earth

    start = time_ns()

    for (year_idx, year), (lat_idx, lat), (lon_idx, lon), (alt_idx, alt), (itype_idx, itype) in tqdm(itertools.product(
        enumerate(years), enumerate(lats), enumerate(lons), enumerate(alts), enumerate(itypes),
    ), total = years.shape[0] * lats.shape[0] * lons.shape[0] * alts.shape[0] * len(itypes)):

        offset = 0.0 if itype == 1 else 6371.2

        _, _, _, _ = get_syn(
            year = year,
            lat = float(lat),
            elong = float(lon),
            alt = float(alt) + offset,
            itype = itype,
        )

    duration = (time_ns() - start) * 1e-9
    print(f'duration={duration:f}s')


if __name__ == '__main__':
    main()
