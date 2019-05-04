import numpy as np

import pyIGRF.calculate as calculate

FACT = 180./np.pi


def igrf_value(lat, lon, alt=0., year=2005.):
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
    x, y, z, f = calculate.igrf12syn(year, 1, alt, lat, lon)
    d = FACT * np.arctan2(y, x)
    h = np.sqrt(x * x + y * y)
    i = FACT * np.arctan2(z, h)
    return d, i, h, x, y, z, f


def igrf_variation(lat, lon, alt=0., year=2005):
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
    x1, y1, z1, f1 = calculate.igrf12syn(year-1, 1, alt, lat, lon)
    x2, y2, z2, f2 = calculate.igrf12syn(year+1, 1, alt, lat, lon)
    x, y, z, f = (x1+x2)/2, (y1+y2)/2, (z1+z2)/2, (f1+f2)/2
    dx, dy, dz, df = (x2-x1)/2, (y2-y1)/2, (z2-z1)/2, (f2-f1)/2
    h = np.sqrt(x * x + y * y)

    dd = (FACT * (x * dy - y * dx)) / (h * h)
    dh = (x * dx + y * dy) / h
    ds = (FACT * (h * dz - z * dh)) / (f * f)
    df = (h * dh + z * dz) / f
    return dd, ds, dh, dx, dy, dz, df
