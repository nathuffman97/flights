from io import StringIO

from src.data_scraping.__apis__.inserter import Inserter
import json
import os
import importlib

class DB:

    def __init__(self, path):
        self.ins = Inserter(path)
        self.commands = self._get_insertions(path)
        self.CLASS_NAME = 'src.data_scraping.factories.ins_dict_factory'
        self.flights = ''
        self.cflight = ''
        self.trip = ''

    def insert_trip_data(self, trip_list):
        flight = list()
        trip = list()
        cflight = list()
        for trip_ in trip_list:
            print(trip_)
            for solution in trip_:
                keys = {'trip': list(), 'flight': list()}
                for name, command in self.commands.items():
                    args, key = self._get_function(name).__call__(solution)
                    locals().get(name).append(args)
                    keys[name].extend(key)
                cflight.extend(self._add_connecting_flight(keys))
        self._insert_CSV(flight, trip, cflight)

    def _add_connecting_flight(self, keys):
        cflight = list()
        for flight_id in keys['flight']:
            cflight.append('{},{}'.format(keys['trip'][0], flight_id))
        return cflight

    def _get_insertions(self, path):
        with open(os.path.join(path, 'insert_commands.json')) as file:
            return dict(json.load(file))

    def _get_function(self, name):
        module = importlib.import_module(self.CLASS_NAME)
        function = getattr(module, name)
        return function

    def _insert_CSV(self, flights, trips, connectingflights):
        flight = StringIO(''.join(flights))
        trip = StringIO(''.join(trips))
        connectingflight = StringIO('\n'.join(connectingflights))
        self.ins.insert_csv(flight, 'flight')
        self.ins.insert_csv(trip, 'trip')
        self.ins.insert_csv(connectingflight, 'connectingflight')
