import json
from math import sin, cos, atan2, sqrt, radians

_filepath = ".\\files\\bars.json"


def load_data(filepath):
    with open(filepath, "r", encoding="utf8") as _f:
        return json.load(_f)


def parse_data(data):
    _dict = {}
    _arr = []
    for elem in data['features']:
        _dict['sCount'] = elem['properties']['Attributes']['SeatsCount']
        _dict['name'] = elem['properties']['Attributes']['Name']
        _dict['longitude'] = elem['geometry']['coordinates'][0]
        _dict['latitude'] = elem['geometry']['coordinates'][1]
        _arr.append(_dict.copy())
    return _arr


def get_seats(pdata):
    seatsCount = pdata["sCount"]
    return seatsCount


def get_biggest_bar(pdata):
    return max(pdata, key=get_seats)['name']


def get_smallest_bar(pdata):
    return min(pdata, key=get_seats)['name']


def get_distance(lng_curr, ltt_curr, lng_src, ltt_src):
    R = 6371.0  # earth radius
    ltt_curr = radians(ltt_curr)
    ltt_src = radians(ltt_src)
    lng_src = radians(lng_src)
    lng_curr = radians(lng_curr)
    diff_longitude = lng_src - lng_curr
    diff_latitude = ltt_src - ltt_curr
    a = (sin(diff_latitude))**2+cos(ltt_src)*cos(ltt_curr)*(sin(diff_longitude/2))**2
    c = 2 * atan2 (sqrt(a), sqrt(1-a))
    return R*c


def get_closest_bar(pdata, longitude, latitude):
    distance = 6371*2  # Earth radius * 2
    bar_name = ""
    for elem in pdata:
        _distance = get_distance(longitude, latitude, elem["longitude"], elem["latitude"])
        if _distance < distance:
            distance = _distance
            bar_name = elem["name"]
    return bar_name


if __name__ == '__main__':
    _data = load_data(_filepath)
    _pdata = parse_data(_data)

    while True:
        try:
            print("Input your coordinates")
            longitude = input("Longitude:")
            latitude = input("Latitude:")
            print("Ur coordinates: ", longitude, " ", latitude)
            print("closest: ", get_closest_bar(_pdata, float(longitude), float(latitude)))
        except ValueError:
            print("please input number in correct format. Example: 34.3234235")
            continue
        else:
            break

    print("Bar with most seats: ", get_biggest_bar(_pdata))
    print("Bar with least seats: ", get_smallest_bar(_pdata))

