# -*- coding: utf-8 -*-

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import itertools
from multiprocessing import cpu_count
import os
import shutil
from subprocess import Popen
from typing import Union
from urllib.request import urlopen, Request

import numpy as np
from pexpect import spawn
from tqdm import tqdm
from typeguard import typechecked
import zarr

from pyIGRF import get_syn


CMD = "igrf13"
DATA = "data.zarr"
DTYPE = 'f4'
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
    assert 0.0 <= lon < 360.0

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

    if itype == 1:
        proc.expect(' Enter altitude in km')
    else:
        proc.expect(r' Enter radial distance in km \(>3485 km\)')
    proc.sendline(f'{alt:0.03f}')

    proc.expect(' Enter latitude & longitude in decimal degrees')
    proc.sendline(f'{lat:0.03f}')
    proc.sendline(f'{lon:0.03f}')

    proc.expect(r' Enter place name \(20 characters maximum\)')
    proc.sendline('')

    try:
        proc.expect(r' Do you want values for another date \& position\? \(y/n\)')
        reply = _parse_reply(proc.before.decode('utf-8'))
        proc.sendline('n')
    except Exception as e:
        print(proc.before.decode('utf-8'))
        raise ValueError(year, alt, lat, lon, itype) from e

    proc.wait()

    return reply


@typechecked
def _compute_arrays(
    data_fn: str,
    year_step: float = 2.0, # 2.0
    lat_step: float = 20.0, # 20.0 / 4.5
    lon_step: float = 20.0, # 20.0 / 4.5
    alt_step: float = 50.0, # 50.0 / 25.0
    parallel: bool = True,
):

    years = np.arange(1900.0, 2030.0 + year_step, year_step, dtype = DTYPE)
    lats = np.arange(-90.0, 90.0 + lat_step, lat_step, dtype = DTYPE)
    lons = np.arange(0.0, 360.0, lon_step, dtype = DTYPE)
    alts = np.arange(-100.0, 400.0 + alt_step, alt_step, dtype = DTYPE)
    itypes = (1, 2) # above sea level, from centre of Earth

    radius = 6371.2 # km

    columns = ('D', 'I', 'H', 'X', 'Y', 'Z', 'F')
    columns = columns + tuple(f'{column}_SV' for column in columns)

    data = zarr.open(data_fn, mode = 'w')
    field = data.create_dataset(
        name = 'field',
        shape = (years.shape[0], lats.shape[0], lons.shape[0], alts.shape[0], len(itypes), len(columns)),
        chunks = (1, lats.shape[0], lons.shape[0], alts.shape[0], len(itypes), len(columns)),
        dtype = DTYPE,
    )
    field.attrs['dims'] = ['years', 'lats', 'lons', 'alts', 'itypes', 'columns']
    field.attrs['columns'] = list(columns)
    field.attrs['radius'] = radius
    data.create_dataset('years', data = years)
    data.create_dataset('lats', data = lats)
    data.create_dataset('lons', data = lons)
    data.create_dataset('alts', data = alts)
    data.create_dataset('itypes', data = np.array(itypes, dtype = 'u4'))

    if parallel:

        with ProcessPoolExecutor(max_workers = cpu_count()) as p:
            tasks = [
                p.submit(
                    _compute_year_array,
                    data_fn = data_fn,
                    year_idx = year_idx,
                    year = float(year),
                    lats = lats,
                    lons = lons,
                    alts = alts,
                    itypes = itypes,
                    columns = columns,
                    radius = radius,
                )
                for year_idx, year in enumerate(years)
            ]
            for task in tqdm(tasks):
                _ = task.result()

    else:

        for year_idx, year in enumerate(tqdm(years)):
            _ = _compute_year_array(
                data_fn = data_fn,
                year_idx = year_idx,
                year = float(year),
                lats = lats,
                lons = lons,
                alts = alts,
                itypes = itypes,
                columns = columns,
                radius = radius,
            )


@typechecked
def _compute_year_array(
    data_fn: str,
    year_idx: int,
    year: float,
    lats: np.array,
    lons: np.array,
    alts: np.array,
    itypes: tuple[int, int],
    columns: tuple[str, ...],
    radius: float,
) -> bool:

    chunk = np.zeros(
        (lats.shape[0], lons.shape[0], alts.shape[0], len(itypes), len(columns)),
        dtype = DTYPE,
    )

    with ThreadPoolExecutor(max_workers = 30) as p:
        tasks = [
            p.submit(
                _compute_llai_value,
                lat_idx,
                lat,
                lon_idx,
                lon,
                alt_idx,
                alt,
                itype_idx,
                itype,
                year,
                radius,
                columns,
                chunk,
            )
            for (lat_idx, lat), (lon_idx, lon), (alt_idx, alt), (itype_idx, itype) in itertools.product(
                enumerate(lats), enumerate(lons), enumerate(alts), enumerate(itypes),
            )
        ]
        for task in tasks:
            _ = task.result()

    data = zarr.open(data_fn, mode = 'a')
    data['field'][year_idx, ...] = chunk

    return True


def _compute_llai_value(
    lat_idx,
    lat,
    lon_idx,
    lon,
    alt_idx,
    alt,
    itype_idx,
    itype,
    year,
    radius,
    columns,
    chunk,
) -> bool:

    elevation = 0.0 if itype == 1 else radius
    field = _compute(
        year = year,
        lat = float(lat),
        lon = float(lon),
        alt = float(alt) + elevation,
        itype = itype,
    )
    for column_idx, column in enumerate(columns):
        chunk[
            lat_idx,
            lon_idx,
            alt_idx,
            itype_idx,
            column_idx,
        ] = field[column]

    return True


@typechecked
def _verify_arrays(
    data_fn: str,
    parallel: bool = True,
):

    data = zarr.open(data_fn, mode = 'r')

    years = data['years'][...]
    lats = data['lats'][...]
    lons = data['lons'][...]
    alts = data['alts'][...]
    itypes = tuple(int(number) for number in data['itypes'][...]) # above sea level, from centre of Earth
    radius = data['field'].attrs['radius'] # km
    columns = tuple(data['field'].attrs['columns'])

    if parallel:

        with ProcessPoolExecutor(max_workers = cpu_count()) as p:
            tasks = [
                p.submit(
                    _verify_year_array,
                    data_fn = data_fn,
                    year_idx = year_idx,
                    year = float(year),
                    lats = lats,
                    lons = lons,
                    alts = alts,
                    itypes = itypes,
                    columns = columns,
                    radius = radius,
                )
                for year_idx, year in enumerate(years)
            ]
            for task in tqdm(tasks):
                _ = task.result()

    else:

        for year_idx, year in enumerate(tqdm(years)):
            _ = _verify_year_array(
                data_fn = data_fn,
                year_idx = year_idx,
                year = float(year),
                lats = lats,
                lons = lons,
                alts = alts,
                itypes = itypes,
                columns = columns,
                radius = radius,
            )


@typechecked
def _verify_year_array(
    data_fn: str,
    year_idx: int,
    year: float,
    lats: np.array,
    lons: np.array,
    alts: np.array,
    itypes: tuple[int, int],
    columns: tuple[str, ...],
    radius: float,
) -> bool:

    data = zarr.open(data_fn, mode = 'r')
    chunk = data['field'][year_idx, ...]

    x_idx = columns.index('X')
    y_idx = columns.index('Y')
    z_idx = columns.index('Z')
    f_idx = columns.index('F')

    for lat_idx, lat in enumerate(lats):
        for lon_idx, lon in enumerate(lons):
            for alt_idx, alt in enumerate(alts):
                for itype_idx, itype in enumerate(itypes):
                    elevation = 0.0 if itype == 1 else radius
                    x, y, z, f = get_syn(
                        year = year,
                        lat = float(lat),
                        elong = float(lon),
                        alt = float(alt) + elevation,
                        itype = itype,
                    )
                    expected = chunk[lat_idx, lon_idx, alt_idx, itype_idx, [x_idx, y_idx, z_idx, f_idx]]
                    computed = np.array((x, y, z, f), dtype = chunk.dtype) # .round()
                    if not np.allclose(expected, computed, atol = 0.5):
                        raise ValueError((
                            f"year={year:f} lat={lat:f} lon={lon:f} alt={alt:f} itype={itype:d}\n"
                            f"expected   = {repr(expected):s}\n"
                            f"computed_r = {repr(computed.round()):s}\n"
                            f"computed   = {repr(computed):s}"
                        ))

    return True


@typechecked
def _parse_reply(reply: str) -> dict[str, float]:

    lines = [
        line.strip()
        for line in reply.split('\n')
        if len(line.strip()) > 0
    ]
    lines = [
        line
        for line in lines
        if not line.startswith('This version') and not line.startswith('values for') and not line[0].isnumeric()
    ]

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
def main(clean: bool = True, parallel: bool = True):

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
        shutil.rmtree(data_fn)
    if not os.path.exists(data_fn):
        _compute_arrays(data_fn, parallel = parallel)

    _verify_arrays(data_fn, parallel = parallel)


if __name__ == '__main__':
    main()
