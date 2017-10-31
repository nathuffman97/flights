import json
import os

from src.data_scraping.__apis__.qpx import QPX
from src.data_scraping.__apis__.textme import Text
from src.data_scraping.__apis__.db_writer import DB


def make_route_dict():
    with open(trip_routes, 'r') as routes_file:
        data = json.load(routes_file)
        for flight in data['Flight']:
            route_dict[flight['depart']] = flight['arrive']




if __name__ == '__main__':
    data_path = os.path.abspath(os.path.join(os.getcwd(), "..", "..", "data"))
    trip_routes = os.path.join(data_path, 'TripRoutes.json')

    # text_api = Text(data_path)
    flight_api = QPX(data_path)
    db = DB(data_path)
    #db._url
    result_dict = flight_api.make_request(depart='SAN', arrive='RDU', date='2017-11-10')
    print(result_dict)
    db.insert_trip_data(result_dict)

    #db_url = get_db_url()
    route_dict = {}

