#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import numpy as np


def load_coeffs(filename):
    """
    load igrf12 coeffs from file
    :param filename: file which save coeffs (str)
    :return: g and h list one by one (list(float))
    """
    gh = []
    gh2arr = []
    with open(filename) as f:
        text = f.readlines()
        for a in text:
            if a[:2] == 'g ' or a[:2] == 'h ':
                b = a.split()[3:]
                b = [float(x) for x in b]
                gh2arr.append(b)
        gh2arr = np.array(gh2arr).transpose()
        N = len(gh2arr)
        for i in range(N):
            if i < 19:
                for j in range(120):
                    gh.append(gh2arr[i][j])
            else:
                for p in gh2arr[i]:
                    gh.append(p)
        gh.append(0)
        return gh


gh = load_coeffs(os.path.dirname(os.path.abspath(__file__)) + '/src/igrf13coeffs.txt')


def get_coeffs(date):
    """
    :param gh: list from load_coeffs
    :param date: float
    :return: list: g, list: h
    """
    if date < 1900.0 or date > 2030.0:
        print('This subroutine will not work with a date of ' + str(date))
        print('Date must be in the range 1900.0 <= date <= 2030.0')
        print('On return [], []')
        return [], []
    elif date >= 2020.0:
        if date > 2025.0:
            # not adapt for the model but can calculate
            print('This version of the IGRF is intended for use up to 2025.0.')
            print('values for ' + str(date) + ' will be computed but may be of reduced accuracy')
        t = date - 2020.0
        tc = 1.0
        #     pointer for last coefficient in pen-ultimate set of MF coefficients...
        ll = 3060+195
        nmx = 13
        nc = nmx * (nmx + 2)
    else:
        t = 0.2 * (date - 1900.0)
        ll = int(t)
        t = t - ll
        #     SH models before 1995.0 are only to degree 10
        if date < 1995.0:
            nmx = 10
            nc = nmx * (nmx + 2)
            ll = nc * ll
        else:
            nmx = 13
            nc = nmx * (nmx + 2)
            ll = int(0.2 * (date - 1995.0))
            #     19 is the number of SH models that extend to degree 10
            ll = 120 * 19 + nc * ll
        tc = 1.0 - t

    g, h = [], []
    temp = ll-1
    for n in range(nmx+1):
        g.append([])
        h.append([])
        if n == 0:
            g[0].append(None)
        for m in range(n+1):
            if m != 0:
                g[n].append(tc*gh[temp] + t*gh[temp+nc])
                h[n].append(tc*gh[temp+1] + t*gh[temp+nc+1])
                temp += 2
                # print(n, m, g[n][m], h[n][m])
            else:
                g[n].append(tc*gh[temp] + t*gh[temp+nc])
                h[n].append(None)
                temp += 1
                # print(n, m, g[n][m], h[n][m])
    return g, h
