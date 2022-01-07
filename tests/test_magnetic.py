# -*- coding: utf-8 -*-

from math import isclose

import pyIGRF

def test_doc():

    doc = pyIGRF.igrf_value.__doc__
    assert isinstance(doc, str)
    assert len(doc) > 0

    doc = pyIGRF.igrf_variation.__doc__
    assert isinstance(doc, str)
    assert len(doc) > 0

def test_compute():

    date = 1999

    lat = 40
    lon = 116
    alt = 300

    expected_value = (
        -5.080158216428891,
        57.85556540804097,
        24750.880520185507,
        24653.65386814849,
        -2191.674582146139,
        39388.39340198416,
        46519.368238551644,
    )
    expected_variation = (
        -0.022800119085463918,
        0.04087715389679826,
        -19.857404366020084,
        -20.65154904740848,
        -8.05224429543091,
        30.777595502899203,
        15.49444079804009,
    )

    computed_value = pyIGRF.igrf_value(lat, lon, alt, date)
    computed_variation = pyIGRF.igrf_variation(lat, lon, alt, date)

    assert all(isclose(a, b) for a, b in zip(expected_value, computed_value))
    assert all(isclose(a, b) for a, b in zip(expected_variation, computed_variation))

def test_coeffs():

    date = 1999

    g, h = pyIGRF.loadCoeffs.get_coeffs(date)

    assert len(g) == 14
    assert len(h) == 14
