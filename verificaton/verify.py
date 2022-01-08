# -*- coding: utf-8 -*-

import os
from subprocess import Popen
from typing import Union
from urllib.request import urlopen, Request

from pexpect import spawn
from typeguard import typechecked


CMD = "igrf13"
FLD = os.path.dirname(__file__)
URL = "https://www.ngdc.noaa.gov/IAGA/vmod/igrf13.f"


@typechecked
def _compute(
    year: float,
    alt: float,
    lat: float,
    lon: float,
    itype: int = 1,
):

    assert itype in (1, 2)

    cmd_fn = os.path.join(FLD, CMD)
    proc = spawn(cmd_fn)

    proc.expect(' or press "Return" for output to screen')
    proc.sendline('') # file or stdout -> stdout

    proc.expect(' 2 - geocentric (shape of Earth is approximated by a sphere)')
    proc.sendline(f'{itype:d}') # coordinate system

    proc.expect(' 3 - values on a latitude/longitude grid at one date')
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

    proc.expect(' Enter place name (20 characters maximum)')
    proc.sendline('')

    reply = proc.before
    print(reply)

    proc.expect(' Do you want values for another date & position? (y/n)')
    proc.sendline('n')


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

    _compute(
        year = 2020.456,
        alt = 99.876,
        lat = 12.345,
        lon = 67.894,
    )


if __name__ == '__main__':
    main()
