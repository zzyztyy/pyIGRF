#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
from typing import Dict, List

import matplotlib.pyplot as plt

from typeguard import typechecked


FLD = os.path.dirname(__file__)


@typechecked
def _get_log(fn: str) -> List[Dict]:

    data = []
    with open(fn, mode = 'r', encoding = 'utf-8') as f:
        for line in f:
            if len(line.strip()) == 0:
                continue
            data.append(json.loads(line.strip()))

    return data


def main():

    FN = os.path.join(FLD, 'data.txt')
    data = _get_log(FN)

    fig, ax = plt.subplots(figsize = (10, 10), dpi = 150)

    for item in data:
        ax.loglog(
            item['iterations'],
            item['durations'],
            label = f"{item['name']:s} | {item['year']:.02f} | {item['itype']:d}",
            linestyle = 'solid' if item['itype'] == 1 else 'dashed',
            color = item['color'],
        )

    ax.legend()
    ax.set_title('pyCRGI benchmark')
    ax.set_xlabel('iterations')
    ax.set_ylabel('time per itertation [s]')
    ax.grid()

    fig.tight_layout()
    fig.savefig(os.path.join(FLD, 'plot.png'))


if __name__ == '__main__':
    main()
