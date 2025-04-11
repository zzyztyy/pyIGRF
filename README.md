# pyIGRF
## What is pyIGRF?  
This is a package of IGRF-14 (International Geomagnetic Reference Field) about python version. 
We can calculate magnetic field intensity and transform coordinate between GeoGraphical and GeoMagnetic.
It don't need any Fortran compiler or NumPy package.  

## How to Install?
Download this package and run install.
>```python setup.py install```

## How to Use it?
First import this package.  
> ```import pyIGRF```

You can calculate magnetic field intensity.   
>```pyIGRF.igrf_value(lat, lon, alt, date)```

or calculate the annual variation of magnetic filed intensity.  
>```pyIGRF.igrf_variation(lat, lon, alt, date)```

the response is 7 float number about magnetic filed which is:  
- D: declination (+ve east)
- I: inclination (+ve down)
- H: horizontal intensity
- X: north component
- Y: east component
- Z: vertical component (+ve down)
- F: total intensity  
*unit: degree or nT*

If you want to use IGRF-13 more flexibly, you can use module *calculate*. 
There is two function which is closer to Fortran. You can change it for different coordination.
>```from pyIGRF import calculate```  

Another module *load_coeffs* can be used to get *g[m][n]* or *h[m][n]* same as that in formula.
>```from pyIGRF.load_coeffs import get_coeffs``` 



## Model Introduction and igrf13-coeffs File Download
https://www.ngdc.noaa.gov/IAGA/vmod/igrf.html
