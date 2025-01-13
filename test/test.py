import numpy as np
import pyIGRF
import datetime as dt

ref0={
	'year': 2025.03288,
	'lat': 0,
	'lon': 0,
	'alt': 500,
	'D': -4.47021,
	'I': -26.58303,
	'H': 21616,
	'X': 21550.0,
	'Y': -1684.8,
	'Z': -10816.4,
	'F': 24171.0,
}
D0,I0,H0,X0,Y0,Z0,F0=pyIGRF.igrf_value(
	lat=ref0['lat'],
	lon=ref0['lon'],
	alt=ref0['alt'],
	year=ref0['year']
	)
print(D0-ref0['D'])
print(I0-ref0['I'])
print(H0-ref0['H'])
print(X0-ref0['X'])
print(Y0-ref0['Y'])
print(Z0-ref0['Z'])
print(F0-ref0['F'])


ref1={
	'year': 2025.03288,
	'lat': 0,
	'lon': 0,
	'alt': 0,
	'D': -4.00974,
	'I': -30.1659,
	'H': 27523.0,
	'X': 27455.6,
	'Y': -1924.6,
	'Z': -15996.8,
	'F': 31834.1
}
D1,I1,H1,X1,Y1,Z1,F1=pyIGRF.igrf_value(
	lat=ref1['lat'],
	lon=ref1['lon'],
	alt=ref1['alt'],
	year=ref1['year']
	)
print(D1-ref1['D'])
print(I1-ref1['I'])
print(H1-ref1['H'])
print(X1-ref1['X'])
print(Y1-ref1['Y'])
print(Z1-ref1['Z'])
print(F1-ref1['F'])

ref3={
	'year': 2020.0,
	'lat': 0,
	'lon': 0,
	'alt': 500,
	'D': -5.09983,
	'I': -26.52093,
	'H': 21697.7,
	'X': 21611.8,
	'Y': -1928.7,
	'Z': -10828.0,
	'F': 24249.4
}
D3,I3,H3,X3,Y3,Z3,F3=pyIGRF.igrf_value(
	lat=ref3['lat'],
	lon=ref3['lon'],
	alt=ref3['alt'],
	year=ref3['year']
	)
print(D3-ref3['D'])
print(I3-ref3['I'])
print(H3-ref3['H'])
print(X3-ref3['X'])
print(Y3-ref3['Y'])
print(Z3-ref3['Z'])
print(F3-ref3['F'])

