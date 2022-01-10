# -*- coding: utf-8 -*-

import numpy as np
import pytest

from pyIGRF import array, jited


ITERATIONS = 1_000


@pytest.mark.parametrize(
    "itype, year",
    [(itype, year) for itype in (1, 2) for year in (1910.0, 1990.0, 2000.0, 2027.00)],
)
def test_array_year(itype, year):

    offset = 0.0 if itype == 1 else 6371.2
    random = np.random.default_rng()

    lats = [float(number) for number in random.uniform(low = -90.0, high = 90.0, size = ITERATIONS)]
    lons = [float(number) for number in random.uniform(low = 0.0, high = 360.0, size = ITERATIONS)]
    alts = [float(number) for number in random.uniform(low = -100.0, high = 400.0, size = ITERATIONS)]

    jited_results = []
    for lat, lon, alt in zip(lats, lons, alts):
        jited_results.append(jited.get_syn(
            year = year,
            lat = lat,
            elong = lon,
            alt = alt + offset,
            itype = itype,
        ))
    jited_results = np.array(jited_results, dtype = 'f8')

    lats = np.array(lats, dtype = 'f8')
    lons = np.array(lons, dtype = 'f8')
    alts = np.array(alts, dtype = 'f8')
    array_results = array.get_syn(
        years = year,
        lats = lats,
        elongs = lons,
        alts = alts + offset,
        itype = itype,
    )

    assert np.allclose(jited_results, array_results)
