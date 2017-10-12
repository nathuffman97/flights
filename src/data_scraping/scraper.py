import json
import requests
import html
import os


def make_route_dict():
    with open(trip_routes, 'r') as routes_file:
        data = json.load(routes_file)
        for flight in data['Flight']:
            route_dict[flight['depart']] = flight['arrive']


def generate_request():
    with open(os.path.join(data_path, 'request.json')) as request_file:



def get_API_key():
    key_location = os.path.join(data_path, 'key.json')
    with open(key_location, 'r') as key_file:
        return json.load(key_file)['key']


if __name__ == '__main__':
    data_path = os.path.abspath(os.path.join(os.getcwd(), "..", "..", "data"))
    trip_routes = os.path.join(data_path, 'TripRoutes.json')
    url = 'https://www.googleapis.com/qpxExpress/v1/trips/search?key=' + get_API_key()
    route_dict = {}
    make_route_dict()
    generate_request()