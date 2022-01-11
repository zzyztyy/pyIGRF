# -*- coding: utf-8 -*-

import numpy as np
import pytest

from pyIGRF import array, jited


ITERATIONS = 10_000


@pytest.mark.parametrize(
    "itype, year",
    [(itype, year) for itype in (1, 2) for year in (1910.0, 1990.0, 2000.0, 2027.00)],
)
def test_array_year(itype, year):

    offset = 0.0 if itype == 1 else 6371.2
    random = np.random.default_rng()

    lats = random.uniform(low = -90.0, high = 90.0, size = ITERATIONS).astype('f8')
    lons = random.uniform(low = 0.0, high = 360.0, size = ITERATIONS).astype('f8')
    alts = random.uniform(low = -100.0, high = 400.0, size = ITERATIONS).astype('f8') + offset

    array_results = array.get_syn(
        years = year,
        lats = lats,
        elongs = lons,
        alts = alts,
        itype = itype,
    )

    lats = [float(number) for number in lats]
    lons = [float(number) for number in lons]
    alts = [float(number) for number in alts]

    jited_results = [
        jited.get_syn(
            year = year,
            lat = lat,
            elong = lon,
            alt = alt,
            itype = itype,
        )
        for lat, lon, alt in zip(lats, lons, alts)
    ]

    assert np.allclose(
        np.array(jited_results, dtype = 'f8'),
        array_results,
    )


@pytest.mark.parametrize(
    "itype",
    [1, 2],
)
def test_array_years(itype):

    offset = 0.0 if itype == 1 else 6371.2
    random = np.random.default_rng()

    years = random.uniform(low = 1900.0, high = 2030.0, size = ITERATIONS).astype('f8')
    lats = random.uniform(low = -90.0, high = 90.0, size = ITERATIONS).astype('f8')
    lons = random.uniform(low = 0.0, high = 360.0, size = ITERATIONS).astype('f8')
    alts = random.uniform(low = -100.0, high = 400.0, size = ITERATIONS).astype('f8') + offset

    array_results = array.get_syn(
        years = years,
        lats = lats,
        elongs = lons,
        alts = alts,
        itype = itype,
    )

    years = [float(number) for number in years]
    lats = [float(number) for number in lats]
    lons = [float(number) for number in lons]
    alts = [float(number) for number in alts]

    jited_results = [
        jited.get_syn(
            year = year,
            lat = lat,
            elong = lon,
            alt = alt,
            itype = itype,
        )
        for year, lat, lon, alt in zip(years, lats, lons, alts)
    ]

    assert np.allclose(
        np.array(jited_results, dtype = 'f8'),
        array_results,
    )
