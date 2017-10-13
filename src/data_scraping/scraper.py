import json
import requests
import records
import os
from .textme import Text

def make_route_dict():
    with open(trip_routes, 'r') as routes_file:
        data = json.load(routes_file)
        for flight in data['Flight']:
            route_dict[flight['depart']] = flight['arrive']


def generate_request():
    



def get_api_url():
    key_location = os.path.join(data_path, 'api_url.json')
    with open(key_location, 'r') as key_file:
        return json.load(key_file)['url']


def get_db_url():
    file_loaction = os.path.join(data_path, 'db_url.json')
    with json.load(open(file_loaction)) as data_file:


if __name__ == '__main__':
    data_path = os.path.abspath(os.path.join(os.getcwd(), "..", "..", "data"))
    trip_routes = os.path.join(data_path, 'TripRoutes.json')
    api_url = get_api_url()
    db_url = get_db_url()
    route_dict = {}

    make_route_dict()
    generate_request()
    text_interface = Text(data_path)