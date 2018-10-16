import json
from math import sin, cos, atan2, sqrt, radians
import argparse
import os.path


def load_data_from_json(filepath):
    os.path.isfile(filepath)
    with open(filepath, "r", encoding="utf8") as json_file:
        return json.load(json_file)


def get_bars_from_dict(parsed_data):
    bars = parsed_data["features"]
    return bars


def get_biggest_bar(parsed_data):
    return max(get_bars_from_dict(parsed_data),
               key=lambda item:
               item["properties"]["Attributes"]["SeatsCount"])


def get_smallest_bar(parsed_data):
    return min(get_bars_from_dict(parsed_data),
               key=lambda item:
               item["properties"]["Attributes"]["SeatsCount"])


def get_distance(lon_user, lat_user, lon_src, lat_src):
    # https://stackoverflow.com/a/19412565/8482475
    earth_radius = 6371
    lat_user = radians(lat_user)
    lat_src = radians(lat_src)
    lon_src = radians(lon_src)
    lon_user = radians(lon_user)
    diff_lon = lon_src - lon_user
    diff_lat = lat_src - lat_user
    first_multiplier = \
        (sin(diff_lat))**2+cos(lat_src)*cos(lat_user)*(sin(diff_lon/2))**2
    second_multiplier = \
        2 * atan2(sqrt(first_multiplier), sqrt(1-first_multiplier))
    return earth_radius*second_multiplier


def get_closest_bar(parsed_data, longitude, latitude):
    return min(get_bars_from_dict(parsed_data),
               key=lambda item:
               get_distance(longitude, latitude,
                            item["geometry"]["coordinates"][0],
                            item["geometry"]["coordinates"][1]))


def print_bar(bar):
    # if will need more items, we will just return more (or return dict)
    bar_name = bar["properties"]["Attributes"]["Name"]
    return bar_name


def get_args():
    parser = argparse.ArgumentParser(description="Enter the path directory:")
    parser.add_argument("-file", required=True, help="Path to file")
    return parser.parse_args()


def get_user_input_data():
    try:
        user_input = []
        print("Input your coordinates")
        user_input.append(float(input("Longitude:")))
        user_input.append(float(input("Latitude:")))
        return user_input
    except ValueError:
        return None


if __name__ == "__main__":
    try:
        path = get_args().file
        bars_data = load_data_from_json(path)
    except FileNotFoundError:
        print("File can not be found. Make sure you entered right path")
    except ValueError:
        print("That is not JSON-file")
    else:
        user_coordinates = get_user_input_data()
        if user_coordinates is None:
            print("Coordinates was input in wrong format."
                  "Use this format instead: 34.66661")
        else:
            closest_bar = get_closest_bar(bars_data,
                                          user_coordinates[0],
                                          user_coordinates[1])
            print("Ur coordinates: ", user_coordinates)
            print("closest: ", print_bar(closest_bar))
        biggest_bar = get_biggest_bar(bars_data)
        print("Bar with most seats: ", print_bar(biggest_bar))
        smallest_bar = get_smallest_bar(bars_data)
        print("Bar with least seats: ", print_bar(smallest_bar))
