#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import numpy as np


def loadCoeffs(filename):
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


gh = loadCoeffs(os.path.dirname(os.path.abspath(__file__))+'\\src\\igrf12coeffs.txt')
