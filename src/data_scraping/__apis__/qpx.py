import os
import json
import requests

class QPX:

    def __init__(self, data_path):
        self.data_path = data_path
        self._url_api = self._get_api_url()
        self.header = {'Content-type': 'application/json'}
        self.num_requests = (20,)

    def make_request(self, depart, arrive, date):
        self._package_request(depart, arrive, date)
        self._send_requests()

    def _get_api_url(self):
        key_location = os.path.join(self.data_path, 'api_url.json')
        with open(key_location, 'r') as key_file:
            return json.load(key_file)['url']

    def _package_request(self, depart, arrive, date):
        self.request = {'request': {
            'passengers': {
                'adultCount': 1
            },
            'slice': [
                {
                'origin': depart,
                'destination': arrive,
                'date': date
            }],
            'solutions': self.num_requests[0]
            }
        }

    def _send_requests(self):
        r = requests.post(self._url_api, data=json.dumps(self.request), headers=self.header)
        x = r.json()
        for temp in x['trips']['tripOption']:
            id = temp['id']
            total = temp['saleTotal']
            flight_code = []
            airports = []
            depart_times = []
            for __slice in temp['slice']:
                for segment in __slice['segment']:
                    flight_code.append(segment['flight']['carrier'] + segment['flight']['number'])
                    leg = segment['leg'][0]
                    airports.append(leg['origin'])
                    airports.append(leg['destination'])
                    depart_times.append(leg['departureTime'])
            print(id, total, flight_code, airports, depart_times)
