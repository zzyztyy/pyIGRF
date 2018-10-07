import value
import pyIGRF

if __name__ == '__main__':
    lat = 40
    lon = 116
    alt = 300
    print(value.igrf_variation.__doc__)
    print(pyIGRF.igrf_value(lat, lon, alt, 2006))
