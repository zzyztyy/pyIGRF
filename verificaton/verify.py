# -*- coding: utf-8 -*-

import os
from subprocess import Popen
from typing import Union
from urllib.request import urlopen, Request

import h5py
import numpy as np
from pexpect import spawn
from tqdm import tqdm
from typeguard import typechecked


CMD = "igrf13"
DATA = "data.h5"
FLD = os.path.dirname(__file__)
URL = "https://www.ngdc.noaa.gov/IAGA/vmod/igrf13.f"


@typechecked
def _compute(
    year: float,
    alt: float,
    lat: float,
    lon: float,
    itype: int = 1,
) -> dict[str, float]:

    assert itype in (1, 2)
    assert 1900.0 <= year <= 2030.0
    assert -90.0 <= lat <= 90.0
    assert 0.0 <= lon <= 360.0

    cmd_fn = os.path.join(FLD, CMD)
    proc = spawn(cmd_fn)

    proc.expect(' or press "Return" for output to screen')
    proc.sendline('') # file or stdout -> stdout

    proc.expect(r' 2 - geocentric \(shape of Earth is approximated by a sphere\)')
    proc.sendline(f'{itype:d}') # coordinate system

    proc.expect(r' 3 - values on a latitude\/longitude grid at one date')
    proc.sendline('1') # values at one or more locations & dates

    proc.expect(' 2 - in decimal degrees')
    proc.sendline('2') # decimal degrees

    proc.expect(' Enter date in years A.D.')
    proc.sendline(f'{year:0.03f}')

    proc.expect(' Enter altitude in km')
    proc.sendline(f'{alt:0.03f}')

    proc.expect(' Enter latitude & longitude in decimal degrees')
    proc.sendline(f'{lat:0.03f}')
    proc.sendline(f'{lon:0.03f}')

    proc.expect(r' Enter place name \(20 characters maximum\)')
    proc.sendline('')

    proc.expect(r' Do you want values for another date \& position\? \(y/n\)')
    reply = _parse_reply(proc.before.decode('utf-8'))
    proc.sendline('n')

    proc.wait()

    return reply


@typechecked
def _compute_arrays(
    fn: str,
    year_step: float = 0.25,
    lat_step: float = 0.5,
    lon_step: float = 0.5,
    alt_step: float = 10.0,
):
    """
        'D': -0.8833333333333333,
        'D_SV': 2.0,
        'I': 13.333333333333334,
        'I_SV': 7.0,
        'H': 37151.0,
        'H_SV': 43.0,
        'X': 37144.0,
        'X_SV': 43.0,
        'Y': -723.0,
        'Y_SV': 16.0,
        'Z': 8804.0,
        'Z_SV': 87.0,
        'F': 38180.0,
        'F_SV': 62.0,
    """

    years = np.arange(1900.0, 2030.0 + year_step, year_step, dtype = 'f8')
    lat = np.arange(-90.0, 90.0 + lat_step, dtype = 'f8')
    lon = np.arange(0.0, 360.0 + lon_step, dtype = 'f8')
    alt = np.arange(-10.0, 400.0 + alt_step, alt_step, dtype = 'f8')

    columns = ('D', 'I', 'H', 'X', 'Y', 'Z', 'F')
    columns = columns + tuple(f'{column}_SV' for column in columns)

    data = np.zeros(
        (years.shape[0], lat.shape[0], lon.shape[0], alt.shape[0]),
        dtype = 'f8',
    )


@typechecked
def _parse_reply(reply: str) -> dict[str, float]:

    lines = [
        line.strip()
        for line in reply.split('\n')
        if len(line.strip()) > 0
    ]
    lines.pop(0)

    reply = {}
    for line in lines:

        name, fragment = line.split('=', 1)
        name = name.strip()
        fragment = fragment.strip()

        value, svvalue = fragment.split('SV')
        value = value.strip()

        if name in ('D', 'I'):
            value = value.split()
            value = float(value[0]) + float(value[2]) / 60
        else:
            value, _ = value.split(' ')
            value = float(value)

        svvalue = float(svvalue.split()[1])

        reply[name] = value
        reply[f'{name:s}_SV'] = svvalue

    return reply


@typechecked
def _build(in_fn: str, out_fn: str):

    proc = Popen(['gfortran', in_fn, '-o', out_fn])
    proc.wait()
    assert proc.returncode == 0


@typechecked
def _download(down_url: str, mode: str = "binary") -> Union[str, bytes]:

    assert mode in ("text", "binary")
    assert isinstance(down_url, str)

    httprequest = Request(down_url)

    with urlopen(httprequest) as response:
        assert response.status == 200
        data = response.read()

    if mode == 'text':
        return data.decode('utf-8')

    return data # mode == 'binary'


@typechecked
def main(clean: bool = False):

    src_fn = os.path.join(FLD, f'{CMD:s}.f')
    if clean and os.path.exists(src_fn):
        os.unlink(src_fn)
    if not os.path.exists(src_fn):
        raw = _download(URL)
        with open(src_fn, mode = 'wb') as f:
            f.write(raw)

    cmd_fn = os.path.join(FLD, CMD)
    if clean and os.path.exists(cmd_fn):
        os.unlink(cmd_fn)
    if not os.path.exists(cmd_fn):
        _build(src_fn, cmd_fn)

    data_fn = os.path.join(FLD, DATA)
    if clean and os.path.exists(data_fn):
        os.unlink(data_fn)
    if not os.path.exists(data_fn):
        _compute_arrays(data_fn)


if __name__ == '__main__':
    main()
