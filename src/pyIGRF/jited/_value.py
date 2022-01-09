# -*- coding: utf-8 -*-

from math import atan2, sqrt, pi

from .._debug import typechecked
from ._calculate import get_syn


FACT = 180.0 / pi


@typechecked
def get_value(
    lat: float,
    lon: float,
    alt: float = 0.0,
    year: float = 2005.0,
) -> tuple[float, float, float, float, float, float, float]:
    """
    Computes magnetic field values at given point in space.

    Args:
        lat : Latitude
        lon : Longitude
        alt : Altitude
        year : Between 1900.0 and 2030.0
    Returns:
        D, declination (+ve east);
        I, inclination (+ve down);
        H, horizontal intensity;
        X, north component;
        Y, east component;
        Z, vertical component (+ve down);
        F, total intensity
    """

    x, y, z, f = get_syn(year, 1, alt, lat, lon)

    d = FACT * atan2(y, x)
    h = sqrt(x * x + y * y)
    i = FACT * atan2(z, h)

    return d, i, h, x, y, z, f


@typechecked
def get_variation(
    lat: float,
    lon: float,
    alt: float = 0.0,
    year: float = 2005.0,
) -> tuple[float, float, float, float, float, float, float]:
    """
    Computes annual variation of magnetic field values at given point in space.

    Args:
        lat : Latitude
        lon : Longitude
        alt : Altitude
        year : Between 1900.0 and 2030.0
    Returns:
        D, declination (+ve east);
        I, inclination (+ve down);
        H, horizontal intensity;
        x, north component;
        y, east component;
        Z, vertical component (+ve down);
        F, total intensity
    """

    x1, y1, z1, f1 = get_syn(year - 1, 1, alt, lat, lon)
    x2, y2, z2, f2 = get_syn(year + 1, 1, alt, lat, lon)
    x, y, z, f = (x1 + x2) / 2, (y1 + y2) / 2, (z1 + z2) / 2, (f1 + f2) / 2
    dx, dy, dz, df = (x2 - x1) / 2, (y2 - y1) / 2, (z2 - z1) / 2, (f2 - f1) / 2
    h = sqrt(x * x + y * y)

    dd = (FACT * (x * dy - y * dx)) / (h * h)
    dh = (x * dx + y * dy) / h
    ds = (FACT * (h * dz - z * dh)) / (f * f)
    df = (h * dh + z * dz) / f

    return dd, ds, dh, dx, dy, dz, df
