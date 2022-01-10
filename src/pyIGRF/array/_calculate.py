# -*- coding: utf-8 -*-

from numpy import sin, cos, sqrt, arctan2, pi

import numba as nb
import numpy as np

from ..jited import geodetic2geocentric as _geodetic2geocentric_scalar


FACT = 180.0 / pi


@nb.njit('void(f8[:],f8[:],f8[:],f8[:],f8[:])')
def geodetic2geocentric(theta, alt, gccolat, d, r):
    """
    Conversion from geodetic to geocentric coordinates by using the WGS84 spheroid.

    Args:
        theta : colatitude [rad]
        alt : altitude [km]
        gccolat : geocentric colatitude [rad] (output)
        d : gccolat minus theta [rad] (output)
        r : geocentric radius [km] (output)
    """

    assert theta.shape[0] == alt.shape[0] == gccolat.shape[0] == d.shape[0] == r.shape[0]

    ct = cos(theta)
    st = sin(theta)
    a2 = 40680631.6
    b2 = 40408296.0
    one = a2 * st * st
    two = b2 * ct * ct
    three = one + two
    rho = sqrt(three)
    r[:] = sqrt(alt * (alt + 2.0 * rho) + (a2 * one + b2 * two) / three)
    cd = (alt + rho) / r
    sd = (a2 - b2) / rho * ct * st / r
    one = ct
    ct = ct * cd - st * sd
    st = st * cd + one * sd
    gccolat[:] = arctan2(st, ct)
    d[:] = arctan2(sd, cd)


@nb.njit('void(f8,i8,f8,f8,f8,f8[:,:,:],i8,f8[:])')
def _get_syn(year, itype, alt, lat, elong, gh, sh, xyzf):
    """
    Args:
        year : year A.D. Must be greater than or equal to 1900.0 and
            less than or equal to 2025.0. Warning message is given
            for dates greater than 2020.0. Must be double precision.
        itype : 1 if geodetic (spheroid), 2 if geocentric (sphere)
        alt : height in km above sea level if itype == 1,
            distance from centre of Earth in km if itype == 2 (>3485 km)
        lat : latitude (-90 to 90)
        elong : east-longitude (0 to 360)
        gh : g and h (output)
        sh : number of spherical harmonics plus one (output)
        xyzf : north, east, verical, total; [nT] if isv == 0, [nT/year] if isv == 1 (output)
    """

    xyzf[0], xyzf[1], xyzf[2] = 0., 0., 0.

    if year < 1900.0 or year > 2030.0:
        xyzf[3] = 1.0
        return

    p = np.zeros((105,), dtype = 'f8')
    q = np.zeros((105,), dtype = 'f8')
    cl = np.zeros((13,), dtype = 'f8')
    sl = np.zeros((13,), dtype = 'f8')

    nmx = sh - 1
    kmx = (nmx + 1) * (nmx + 2) // 2 + 1

    colat = 90. - lat
    r = alt

    one = colat / FACT
    ct = cos(one)
    st = sin(one)

    one = elong / FACT
    cl[0] = cos(one)
    sl[0] = sin(one)

    cd = 1.0
    sd = 0.0

    l = 1
    m = 1
    n = 0

    if itype != 2:
        gclat, gclon, r = _geodetic2geocentric_scalar(arctan2(st, ct), alt)
        ct, st = cos(gclat), sin(gclat)
        cd, sd = cos(gclon), sin(gclon)
    ratio = 6371.2 / r
    rr = ratio * ratio

    # computation of Schmidt quasi-normal coefficients p and x(=q)
    p[0] = 1.0
    p[2] = st
    q[0] = 0.0
    q[2] = ct

    fn, gn = n, n - 1
    for k in range(2, kmx):
        if n < m:
            m = 0
            n = n + 1
            rr = rr * ratio
            fn = n
            gn = n - 1

        fm = m
        if m != n:
            gmm = m * m
            one = sqrt(fn * fn - gmm)
            two = sqrt(gn * gn - gmm) / one
            three = (fn + gn) / one
            i = k - n
            j = i - n + 1
            p[k - 1] = three * ct * p[i - 1] - two * p[j - 1]
            q[k - 1] = three * (ct * q[i - 1] - st * p[i - 1]) - two * q[j - 1]
        else:
            if k != 3:
                one = sqrt(1.0 - 0.5 / fm)
                j = k - n - 1
                p[k - 1] = one * st * p[j - 1]
                q[k - 1] = one * (st * q[j - 1] + ct * p[j - 1])
                cl[m - 1] = cl[m - 2] * cl[0] - sl[m - 2] * sl[0]
                sl[m - 1] = sl[m - 2] * cl[0] + cl[m - 2] * sl[0]
        # synthesis of x, y and z in geocentric coordinates
        one = gh[0, n, m] * rr
        if m == 0:
            xyzf[0] = xyzf[0] + one * q[k - 1]
            xyzf[2] = xyzf[2] - (fn + 1.0) * one * p[k - 1]
            l = l + 1
        else:
            two = gh[1, n, m] * rr
            three = one * cl[m - 1] + two * sl[m - 1]
            xyzf[0] = xyzf[0] + three * q[k - 1]
            xyzf[2] = xyzf[2] - (fn + 1.0) * three * p[k-1]
            if st == 0.0:
                xyzf[1] = xyzf[1] + (one * sl[m - 1] - two * cl[m - 1]) * q[k - 1] * ct
            else:
                xyzf[1] = xyzf[1] + (one * sl[m - 1] - two * cl[m - 1]) * fm * p[k - 1] / st
            l = l + 2
        m = m + 1

    # conversion to coordinate system specified by itype
    one = xyzf[0]
    xyzf[0] = xyzf[0] * cd + xyzf[2] * sd
    xyzf[2] = xyzf[2] * cd - one * sd
    xyzf[3] = sqrt(xyzf[0] * xyzf[0] + xyzf[1] * xyzf[1] + xyzf[2] * xyzf[2])


@nb.njit('void(f8[:],i8,f8[:],f8[:],f8[:],f8[:,:,:,:],i8[:],f8[:,:])', parallel = True)
def get_syn_years(years, itype, alts, lats, elongs, ghs, shs, xyzfs):
    """
    This is a synthesis routine for the 12th generation IGRF as agreed
    in December 2014 by IAGA Working Group V-MOD. It is valid 1900.0 to
    2020.0 inclusive. Values for dates from 1945.0 to 2010.0 inclusive are
    definitive, otherwise they are non-definitive.

    To get the other geomagnetic elements (D, I, H and secular
    variations dD, dH, dI and dF) use routines ptoc and ptocsv.

    Adapted from 8th generation version to include new maximum degree for
    main-field models for 2000.0 and onwards and use WGS84 spheroid instead
    of International Astronomical Union 1966 spheroid as recommended by IAGA
    in July 2003. Reference radius remains as 6371.2 km - it is NOT the mean
    radius (= 6371.0 km) but 6371.2 km is what is used in determining the
    coefficients. Adaptation by Susan Macmillan, August 2003 (for
    9th generation), December 2004, December 2009, December 2014.

    Coefficients at 1995.0 incorrectly rounded (rounded up instead of
    to even) included as these are the coefficients published in Excel
    spreadsheet July 2005.

    Args:
        years : year A.D. Must be greater than or equal to 1900.0 and
            less than or equal to 2025.0. Warning message is given
            for dates greater than 2020.0. Must be double precision.
        itype : 1 if geodetic (spheroid), 2 if geocentric (sphere)
        alts : height in km above sea level if itype == 1,
            distance from centre of Earth in km if itype == 2 (>3485 km)
        lats : latitude (-90 to 90)
        elongs : east-longitude (0 to 360)
        ghs : Array of g and h
        shs : Array of number of spherical harmonics plus one
        xyzfs : north, east, verical, total; [nT] if isv == 0, [nT/year] if isv == 1 (output)
    """

    assert itype == 1 or itype == 2
    assert years.shape[0] == alts.shape[0] == lats.shape[0] == elongs.shape[0] == xyzfs.shape[0]
    assert xyzfs.shape[1] == 4

    for idx in nb.prange(years.shape[0]):
        _get_syn(years[idx], itype, alts[idx], lats[idx], elongs[idx], ghs[idx, ...], shs[idx], xyzfs[idx, :])
