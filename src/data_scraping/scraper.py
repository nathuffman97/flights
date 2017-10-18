import json
import os

from src.data_scraping.__apis__.qpx import QPX


def make_route_dict():
    with open(trip_routes, 'r') as routes_file:
        data = json.load(routes_file)
        for flight in data['Flight']:
            route_dict[flight['depart']] = flight['arrive']

def get_db_url():
    file_loaction = os.path.join(data_path, 'db_url.json')
    with json.load(open(file_loaction)) as data_file:
        return data_file['url']


if __name__ == '__main__':
    data_path = os.path.abspath(os.path.join(os.getcwd(), "..", "..", "data"))
    trip_routes = os.path.join(data_path, 'TripRoutes.json')

    # text_api = Text(data_path)
    flight_api = QPX(data_path)

    flight_api.make_request('SAN', 'RDU', '2017-11-10')

    #db_url = get_db_url()
    #route_dict = {}

    #make_route_dict()
