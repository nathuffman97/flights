import json
import requests
import records
import os
from twilio.rest import TwilioRestClient


def make_route_dict():
    with open(trip_routes, 'r') as routes_file:
        data = json.load(routes_file)
        for flight in data['Flight']:
            route_dict[flight['depart']] = flight['arrive']


def generate_request():
    with open(os.path.join(data_path, 'request.json')) as request_file:



def get_api_url():
    key_location = os.path.join(data_path, 'api_url.json')
    with open(key_location, 'r') as key_file:
        return json.load(key_file)['url']


def set_up_twilio():


#def get_db_url():


if __name__ == '__main__':
    data_path = os.path.abspath(os.path.join(os.getcwd(), "..", "..", "data"))
    trip_routes = os.path.join(data_path, 'TripRoutes.json')
    api_url = get_api_url()
    db_url = get_db_url()
    route_dict = {}
    make_route_dict()
    generate_request()
    set_up_twilio()