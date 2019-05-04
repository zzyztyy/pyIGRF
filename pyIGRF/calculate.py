#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
from pyIGRF.loadCoeffs import get_coeffs, gh


FACT = 180./np.pi


def geodetic2geocentric(theta, alt):
    """
    Conversion from geodetic to geocentric coordinates by using the WGS84 spheroid.
    :param theta: colatitude (float, rad)
    :param alt: altitude (float, km)
    :return gccolat: geocentric colatitude (float, rad)
            d: gccolat minus theta (float, rad)
            r: geocentric radius (float, km)
    """
    ct = np.cos(theta)
    st = np.sin(theta)
    a2 = 40680631.6
    b2 = 40408296.0
    one = a2 * st * st
    two = b2 * ct * ct
    three = one + two
    rho = np.sqrt(three)
    r = np.sqrt(alt * (alt + 2.0 * rho) + (a2 * one + b2 * two) / three)
    cd = (alt + rho) / r
    sd = (a2 - b2) / rho * ct * st / r
    one = ct
    ct = ct * cd - st * sd
    st = st * cd + one * sd
    gccolat = np.arctan2(st, ct)
    d = np.arctan2(sd, cd)
    return gccolat, d, r


def igrf12syn(date, itype, alt, lat, elong):
    """
     This is a synthesis routine for the 12th generation IGRF as agreed
     in December 2014 by IAGA Working Group V-MOD. It is valid 1900.0 to
     2020.0 inclusive. Values for dates from 1945.0 to 2010.0 inclusive are
     definitive, otherwise they are non-definitive.
   INPUT
     date  = year A.D. Must be greater than or equal to 1900.0 and
             less than or equal to 2025.0. Warning message is given
             for dates greater than 2020.0. Must be double precision.
     itype = 1 if geodetic (spheroid)
     itype = 2 if geocentric (sphere)
     alt   = height in km above sea level if itype = 1
           = distance from centre of Earth in km if itype = 2 (>3485 km)
     lat = latitude (-90~90)
     elong = east-longitude (0-360)
     alt, colat and elong must be double precision.
   OUTPUT
     x     = north component (nT) if isv = 0, nT/year if isv = 1
     y     = east component (nT) if isv = 0, nT/year if isv = 1
     z     = vertical component (nT) if isv = 0, nT/year if isv = 1
     f     = total intensity (nT) if isv = 0, rubbish if isv = 1

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
    """

    p, q, cl, sl = [0.] * 105, [0.] * 105, [0.] * 13, [0.] * 13
    x, y, z = 0., 0., 0.

    if date < 1900.0 or date > 2025.0:
        f = 1.0
        print('This subroutine will not work with a date of ' + str(date))
        print('Date must be in the range 1900.0 <= date <= 2025.0')
        print('On return f = 1.0, x = y = z = 0')
        return x, y, z, f

    g, h = get_coeffs(date)
    nmx = len(g)-1
    kmx = (nmx + 1) * (nmx + 2) // 2 + 1

    colat = 90-lat
    r = alt

    one = colat / FACT
    ct = np.cos(one)
    st = np.sin(one)

    one = elong / FACT
    cl[0] = np.cos(one)
    sl[0] = np.sin(one)

    cd = 1.0
    sd = 0.0

    l = 1
    m = 1
    n = 0

    if itype != 2:
        gclat, gclon, r = geodetic2geocentric(np.arctan2(st, ct), alt)
        ct, st = np.cos(gclat), np.sin(gclat)
        cd, sd = np.cos(gclon), np.sin(gclon)
    ratio = 6371.2 / r
    rr = ratio * ratio

    #     computation of Schmidt quasi-normal coefficients p and x(=q)
    p[0] = 1.0
    p[2] = st
    q[0] = 0.0
    q[2] = ct

    fn, gn = n, n-1
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
            one = np.sqrt(fn * fn - gmm)
            two = np.sqrt(gn * gn - gmm) / one
            three = (fn + gn) / one
            i = k - n
            j = i - n + 1
            p[k - 1] = three * ct * p[i - 1] - two * p[j - 1]
            q[k - 1] = three * (ct * q[i - 1] - st * p[i - 1]) - two * q[j - 1]
        else:
            if k != 3:
                one = np.sqrt(1.0 - 0.5 / fm)
                j = k - n - 1
                p[k-1] = one * st * p[j-1]
                q[k-1] = one * (st * q[j-1] + ct * p[j-1])
                cl[m-1] = cl[m - 2] * cl[0] - sl[m - 2] * sl[0]
                sl[m-1] = sl[m - 2] * cl[0] + cl[m - 2] * sl[0]
        #     synthesis of x, y and z in geocentric coordinates
        one = g[n][m] * rr
        if m == 0:
            x = x + one * q[k - 1]
            z = z - (fn + 1.0) * one * p[k - 1]
            l = l + 1
        else:
            two = h[n][m] * rr
            three = one * cl[m-1] + two * sl[m-1]
            x = x + three * q[k-1]
            z = z - (fn + 1.0) * three * p[k-1]
            if st == 0.0:
                y = y + (one * sl[m - 1] - two * cl[m - 1]) * q[k - 1] * ct
            else:
                y = y + (one * sl[m-1] - two * cl[m-1]) * fm * p[k-1] / st
            l = l + 2
        m = m+1

    #     conversion to coordinate system specified by itype
    one = x
    x = x * cd + z * sd
    z = z * cd - one * sd
    f = np.sqrt(x * x + y * y + z * z)
    return x, y, z, f
