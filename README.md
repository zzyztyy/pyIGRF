# pyIGRF
## What is pyIGRF?  
This is a package of IGRF-12 (International Geomagnetic Reference Field) about python version.
It don't need any Fortran compiler.
## How to Use it?
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
## Model Introduction and igrf12-coeffs File Download
https://www.ngdc.noaa.gov/IAGA/vmod/igrf.html
