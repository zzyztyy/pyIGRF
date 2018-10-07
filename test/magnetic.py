import value
import pyIGRF

if __name__ == '__main__':
    lat = 40
    lon = 116
    alt = 300
    date = 2025
    print(value.igrf_variation.__doc__)
    print(pyIGRF.igrf_value(lat, lon, alt, date))
