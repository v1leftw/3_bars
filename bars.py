import json
from math import sin, cos, atan2, sqrt, radians
import argparse
import os.path

EARTH_RADIUS = 6371


def load_data_from_json(filepath):
    if os.path.isfile(filepath):
        try:
            with open(filepath, "r", encoding="utf8") as json_file:
                return json.load(json_file)
        except ValueError as exception:
            # raising different exception to handle ValueError from input
            raise TypeError from exception
    else:
        raise FileNotFoundError


def get_items_from_json(parsed_data):
    bars_data = parsed_data["features"]
    return bars_data


def get_biggest_bar(parsed_data):
    return max(get_items_from_json(parsed_data),
               key=lambda item: item["properties"]["Attributes"]["SeatsCount"])


def get_smallest_bar(parsed_data):
    return min(get_items_from_json(parsed_data),
               key=lambda item: item["properties"]["Attributes"]["SeatsCount"])


# https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
'''
    function get_distance():
    ltt_curr = current latitude (user-inputted)
    ltt_scr = latitude from json-file (source)
    lng_curr = current longitude (user-inputted)
    lng_src = latitude from json-file (source)
'''


def get_distance(lng_curr, ltt_curr, lng_src, ltt_src):
    ltt_curr = radians(ltt_curr)
    ltt_src = radians(ltt_src)
    lng_src = radians(lng_src)
    lng_curr = radians(lng_curr)
    diff_lng = lng_src - lng_curr
    diff_ltt = ltt_src - ltt_curr
    first_multiplier = \
        (sin(diff_ltt))**2+cos(ltt_src)*cos(ltt_curr)*(sin(diff_lng/2))**2
    second_multiplier = \
        2 * atan2(sqrt(first_multiplier), sqrt(1-first_multiplier))
    return EARTH_RADIUS*second_multiplier


def get_closest_bar(parsed_data, longitude, latitude):
    distance = EARTH_RADIUS*2  # Polar radius
    bar = {}
    for elem in get_items_from_json(parsed_data):
        distance_to_closest_bar = \
            get_distance(longitude, latitude,
                         elem["geometry"]["coordinates"][0],
                         elem["geometry"]["coordinates"][1])
        if distance_to_closest_bar < distance:
            distance = distance_to_closest_bar
            bar = elem
    return bar, distance


def get_path_to_file():
    parser = argparse.ArgumentParser(description="Enter the path directory:")
    parser.add_argument("-file", required=True, help="Path to file")
    path = parser.parse_args()
    return path.file


if __name__ == '__main__':
    try:
        json_data = load_data_from_json(get_path_to_file())
        print("Input your coordinates")
        user_longitude = input("Longitude:")
        user_latitude = input("Latitude:")
        closest_bar, distance_to_bar = \
            get_closest_bar(json_data,
                            float(user_longitude), float(user_latitude))
        print("Ur coordinates: ", user_longitude, " ", user_latitude)
        print("closest: ", closest_bar["properties"]["Attributes"]["Name"],
              " distance is: ",
              "{:9.2f}".format(distance_to_bar), "km")
        biggest_bar = get_biggest_bar(json_data)
        print("Bar with most seats: ",
              biggest_bar["properties"]["Attributes"]["Name"])
        smallest_bar = get_smallest_bar(json_data)
        print("Bar with least seats: ",
              smallest_bar["properties"]["Attributes"]["Name"])
    except FileNotFoundError:
        print("File can not be found. Make sure you entered right path")
    except TypeError:
        print("It is not a JSON-file")
    except ValueError:
        print("Please input number in correct format. Example: 34.342554")
