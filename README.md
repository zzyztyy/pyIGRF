# pyIGRF - forked

**This is a cleaned-up and modernized fork of ``pyIGRF``. Be aware that there are a number of small function and module name differences to the original ``pyIGRF`` package. The fork's main goals are speed and ease of maintainability. This is work in progress.**

## What is pyIGRF?

`pyIGRF` is a Python package offering the IGRF-13 (International Geomagnetic Reference Field) model. You can use it to calculate the magnetic field's intensity and to transform coordinates between GeoGraphical and GeoMagnetic. The package does not require any Fortran compiler - it is pure Python.

## How to Install?

Use pip to install the latest development version from Github:

```bash
pip install git+https://github.com/pleiszenburg/pyIGRF.git@develop
```

## How to Use it?

First import the package:

```python
import pyIGRF
```

You can calculate the magnetic field's intensity:

```python
pyIGRF.get_value(lat, lon, alt, date)
```

You can calculate the annual variation of the magnetic field's intensity:

```python
pyIGRF.get_variation(lat, lon, alt, date)
```

The return value is a tuple of seven floating point numbers representing the local magnetic field:

- D: declination (+ve east)
- I: inclination (+ve down)
- H: horizontal intensity
- X: north component
- Y: east component
- Z: vertical component (+ve down)
- F: total intensity

*units: degree or nT*

If you want to use the IGRF-13 model in a more flexible manner, you can use the functions `geodetic2geocentric` and `igrf12syn`. They are somewhat closer to the original Fortran implementation.

Another function, `get_coeffs`, can be used to get `g[m][n]` or `h[m][n]` corresponding to the IGRF's formula.

## References

- [Model introduction and IGRF-13 coefficients file download at NOAA](https://www.ngdc.noaa.gov/IAGA/vmod/igrf.html)
