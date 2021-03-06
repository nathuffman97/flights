import os
import json
from datetime import date
import requests

class QPX:

    def __init__(self, data_path):
        self.data_path = data_path
        self._url_api = self._get_api_url()
        self.header = {'Content-type': 'application/json'}
        self.num_requests = (100,)

    def make_request(self, depart, arrive, date):
        self._package_request(depart, arrive, date)
        return self._send_requests(depart, arrive)

    def _get_api_url(self):
        key_location = os.path.join(self.data_path, 'api_url.json')
        with open(key_location, 'r') as key_file:
            return json.load(key_file)['url']

    def _package_request(self, depart, arrive, date):
        self.request = {'request': {
            'passengers': {
                'adultCount': 1,
            },
            'slice': [
                {
                    'origin': depart,
                    'destination': arrive,
                    'date': date,
            }],
                'solutions': self.num_requests[0]
            }
        }

    def _send_requests(self, depart, arrive):
        response = self._package_response()
        response = response['trips']
        ret = []
        for temp in response['tripOption']:
            curr_dict = {}
            curr_dict['origin'] = depart
            curr_dict['destination'] = arrive
            self._add_root_data(curr_dict, temp)
            self._create_data_lists(curr_dict)
            for __slice in temp['slice']:
                for segment in __slice['segment']:
                    self._add_flight_data(curr_dict, segment)
            ret.append(curr_dict)
        return ret

    def _package_response(self):
        x = requests.post(self._url_api, data=json.dumps(self.request), headers=self.header)
        response = x.json()
        del response['kind']
        return response

    def _add_flight_data(self, ret, segment):
        ret['flight_code'].append(segment['flight']['carrier'] + segment['flight']['number'])
        leg = segment['leg'][0]
        ret['airports'].extend([leg['origin'], leg['destination']])
        ret['depart_times'].append(leg['departureTime'])

    def _create_data_lists(self, ret):
        ret['flight_code'] = []
        ret['airports'] = []
        ret['depart_times'] = []

    def _add_root_data(self, ret, temp):
        ret['id'] = temp['id']
        ret['bdate'] = date.today().strftime('%Y-%m-%d')
        ret['total'] = temp['saleTotal']

