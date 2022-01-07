# -*- coding: utf-8 -*-

from math import atan2, sqrt, pi

from ._calculate import igrf12syn
from ._typeguard import typechecked


FACT = 180.0 / pi


@typechecked
def igrf_value(
    lat: float,
    lon: float,
    alt: float = 0.0,
    year: float = 2005.0,
) -> tuple[float, float, float, float, float, float, float]:
    """
    :return
         D is declination (+ve east)
         I is inclination (+ve down)
         H is horizontal intensity
         X is north component
         Y is east component
         Z is vertical component (+ve down)
         F is total intensity
    """

    x, y, z, f = igrf12syn(year, 1, alt, lat, lon)

    d = FACT * atan2(y, x)
    h = sqrt(x * x + y * y)
    i = FACT * atan2(z, h)

    return d, i, h, x, y, z, f


@typechecked
def igrf_variation(
    lat: float,
    lon: float,
    alt: float = 0.0,
    year: float = 2005.0,
) -> tuple[float, float, float, float, float, float, float]:
    """
         Annual variation
         D is declination (+ve east)
         I is inclination (+ve down)
         H is horizontal intensity
         x is north component
         y is east component
         Z is vertical component (+ve down)
         F is total intensity
    """

    x1, y1, z1, f1 = igrf12syn(year - 1, 1, alt, lat, lon)
    x2, y2, z2, f2 = igrf12syn(year + 1, 1, alt, lat, lon)
    x, y, z, f = (x1 + x2) / 2, (y1 + y2) / 2, (z1 + z2) / 2, (f1 + f2) / 2
    dx, dy, dz, df = (x2 - x1) / 2, (y2 - y1) / 2, (z2 - z1) / 2, (f2 - f1) / 2
    h = sqrt(x * x + y * y)

    dd = (FACT * (x * dy - y * dx)) / (h * h)
    dh = (x * dx + y * dy) / h
    ds = (FACT * (h * dz - z * dh)) / (f * f)
    df = (h * dh + z * dz) / f

    return dd, ds, dh, dx, dy, dz, df
