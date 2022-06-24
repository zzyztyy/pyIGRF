# -*- coding: utf-8 -*-

from math import isclose

import pytest

from pyCRGI.pure import (
    get_coeffs as pure_get_coeffs,
    get_value as pure_get_value,
    get_variation as pure_get_variation,
)
from pyCRGI.jited import (
    get_coeffs as jited_get_coeffs,
    get_value as jited_get_value,
    get_variation as jited_get_variation,
)
from pyCRGI.jited2 import (
    get_coeffs as jited2_get_coeffs,
    get_value as jited2_get_value,
    get_variation as jited2_get_variation,
)


@pytest.mark.parametrize(
    "get_value, get_variation",
    [(pure_get_value, pure_get_variation), (jited_get_value, jited_get_variation), (jited2_get_value, jited2_get_variation)]
)
def test_doc(get_value, get_variation):

    doc = get_value.__doc__
    assert isinstance(doc, str)
    assert len(doc) > 0

    doc = get_variation.__doc__
    assert isinstance(doc, str)
    assert len(doc) > 0


@pytest.mark.parametrize(
    "get_value, get_variation",
    [(pure_get_value, pure_get_variation), (jited_get_value, jited_get_variation), (jited2_get_value, jited2_get_variation)]
)
def test_compute(get_value, get_variation):

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

    computed_value = get_value(lat, lon, alt, date)
    computed_variation = get_variation(lat, lon, alt, date)

    assert all(isclose(a, b) for a, b in zip(expected_value, computed_value))
    assert all(isclose(a, b) for a, b in zip(expected_variation, computed_variation))


@pytest.mark.parametrize(
    "get_coeffs",
    [pure_get_coeffs, jited_get_coeffs, jited2_get_coeffs]
)
def test_coeffs(get_coeffs):

    date = 1999

    g, h = get_coeffs(date)

    assert len(g) == 14
    assert len(h) == 14
