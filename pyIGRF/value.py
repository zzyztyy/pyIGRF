import numpy as np

import caculate

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
    X, Y, Z, F = caculate.igrf12syn(0, year, 1, alt, lat, lon)
    D = FACT * np.arctan2(Y, X)
    H = np.sqrt(X * X + Y * Y)
    I = FACT * np.arctan2(Z, H)
    return D, I, H, X, Y, Z, F


def igrf_variation(lat, lon, alt=0., year=2005):
    """
         Annual variation
         D is declination (+ve east)
         I is inclination (+ve down)
         H is horizontal intensity
         X is north component
         Y is east component
         Z is vertical component (+ve down)
         F is total intensity
    """
    X, Y, Z, F = caculate.igrf12syn(0, year, 1, alt, lat, lon)
    H = np.sqrt(X * X + Y * Y)
    DX, DY, DZ, DF = caculate.igrf12syn(1, year, 1, alt, lat, lon)
    DD = (60.0 * FACT * (X * DY - Y * DX)) / (H * H)
    DH = (X * DX + Y * DY) / H
    DS = (60.0 * FACT * (H * DZ - Z * DH)) / (F * F)
    DF = (H * DH + Z * DZ) / F
    return DD, DS, DH, DX, DY, DZ, DF
