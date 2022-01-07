import pyIGRF

if __name__ == '__main__':
    lat = 40
    lon = 116
    alt = 300
    date = 1999
    print(pyIGRF.igrf_value.__doc__)
    print(pyIGRF.igrf_variation.__doc__)
    print(pyIGRF.igrf_value(lat, lon, alt, date))
    print(pyIGRF.igrf_variation(lat, lon, alt, date))
    g, h = pyIGRF.loadCoeffs.get_coeffs(date)
    print(len(g))
    print(len(h))
