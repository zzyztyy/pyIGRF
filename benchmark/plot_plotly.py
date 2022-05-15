#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
from typing import Dict, List

import plotly.graph_objs as go

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

    traces = []
    for item in data:
        traces.append(go.Scatter(
            x = item['iterations'],
            y = item['durations'],
            mode = "lines+markers",
            name = f"{item['name']:s} | {item['year']:.02f} | {item['itype']:d}",
            line = dict(
                dash = None if item['itype'] == 1 else 'dash',
                color = 'rgba(%d,%d,%d,%d)' % tuple([ch * 255 for ch in item['color']]),
            ),
        ))

    # ax.set_title('pyCRGI benchmark')
    # ax.set_xlabel('iterations')
    # ax.set_ylabel('time per itertation [s]')

    layout = go.Layout(
        autosize=True,
        showlegend=True,
        legend=dict(
            yanchor="top",
            xanchor="right",
            x=1.0,
            y=1.0,
            borderwidth=1,
        ),
        xaxis=dict(
            showgrid=True,
            zeroline=True,
            showline=True,
            mirror="ticks",
            gridwidth=1,
            zerolinewidth=2,
            linewidth=2,
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=True,
            showline=True,
            mirror="ticks",
            gridwidth=1,
            zerolinewidth=2,
            linewidth=2,
        ),
    )

    fig = go.Figure(
        data = traces,
        layout = layout,
    )
    fig.update_xaxes(type = "log")
    fig.update_yaxes(type = "log")

    # show_link = False,
    # output_type = "div",
    # include_plotlyjs = False,
    fig.write_html(os.path.join(FLD, 'plot.htm'))

if __name__ == '__main__':
    main()
