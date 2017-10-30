import argparse
import os
import json

import parser
import requests

class QPX:

    def __init__(self, data_path):
        self.data_path = data_path
        self._url_api = self._get_api_url()
        self.header = {'Content-type': 'application/json'}
        self.num_requests = (500,)

    def make_request(self, **kwargs):
        arrive, date, depart = self._confirm_valid_input(kwargs)
        o_args = self.get_optional_args(kwargs)
        self._package_request(depart, arrive, date)
        return self._send_requests()

    def _confirm_valid_input(self, kwargs):
        if ('depart', 'arrive', 'date' in kwargs):
            depart = kwargs['depart']
            arrive = kwargs['arrive']
            date = kwargs['date']
        else:
            raise TypeError('Values of arrive, depart, and date are required!')
        return arrive, date, depart

    def _get_api_url(self):
        key_location = os.path.join(self.data_path, 'api_url.json')
        with open(key_location, 'r') as key_file:
            return json.load(key_file)['url']

    def _package_request(self, param_dict):
        self.request = {'request': {
            'passengers': {
                'adultCount': int(param_dict['a_count']),
                'childCount': int(param_dict['c_count']),
                'seniorCount': int(param_dict['s_count'])
            },
            'slice': [
                {
                    'origin': param_dict['depart'],
                    'destination': param_dict['arrive'],
                    'date': param_dict['date'],
                    'permittedDepartTime':
                        {
                            'kind': 'qpxexpress#timeOfDayRange',
                            'earliestTime': param_dict['d_e_time'],
                            'latestTime':  param_dict['d_l_time']
                        },
                    'permittedArrivalTime':
                        {
                            'kind': 'qpxexpress#timeOfDayRange',
                            'earliestTime': param_dict['a_e_time'],
                            'latestTime': param_dict['a_l_time']
                        }

            }],
            'maxPrice': param_dict['maxPrice'],
            'solutions': self.num_requests[0]
            }
        }

    def _send_requests(self):
        response = self._package_response()
        ret = {}
        for trip in range(len(response)):
            ret[trip] = {}
            for temp in response['trips']['tripOption']:
                self._add_root_data(ret, temp, trip)
                self._create_data_lists(ret, trip)
                for __slice in temp['slice']:
                    for segment in __slice['segment']:
                        self._add_flight_data(ret, segment, trip)
        return ret

    def _package_response(self):
        x = requests.post(self._url_api, data=json.dumps(self.request), headers=self.header)
        response = x.json()
        del response['kind']
        return response

    def _add_flight_data(self, ret, segment, trip):
        ret[trip]['flight_code'].append(segment['flight']['carrier'] + segment['flight']['number'])
        leg = segment['leg'][0]
        ret[trip]['airports'].extend([leg['origin'], leg['destination']])
        ret[trip]['depart_times'].append(leg['departureTime'])

    def _create_data_lists(self, ret, trip):
        ret[trip]['flight_code'] = []
        ret[trip]['airports'] = []
        ret[trip]['depart_times'] = []

    def _add_root_data(self, ret, temp, trip):
        ret[trip]['id'] = temp['id']
        ret[trip]['total'] = temp['saleTotal']

    def get_optional_args(self, kwargs):
        ret = {}
        if('cabin' in kwargs):
            ret['cabin'] = kwargs['cabin']
        else:
            ret['cab'] = 'coach'
        args = 
