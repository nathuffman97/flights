from src.data_scraping.__apis__.inserter import Inserter
import json
import os
import importlib


class DB:

    def __init__(self, path):
        self.ins = Inserter(path)
        self.commands = self._get_insertions(path)
        self.CLASS_NAME = 'src.data_scraping.factories.ins_dict_factory'

    def insert_trip_data(self, data_dict):
        for name, command in self.commands.items():
            arg_list = self._get_function(name).__call__(data_dict)  # Use reflection to invoke a packaging method
            print(arg_list)
            # self.ins.prepare_command( """PREPARE {} AS {}""".format(name, command))
            # for arg in arg_list:
                # self.ins.execute_command(name, arg)



    def _get_insertions(self, path):
        with open(os.path.join(path, 'insert_commands.json')) as file:
            return dict(json.load(file))

    def _get_function(self, name):
        module = importlib.import_module(self.CLASS_NAME)
        function = getattr(module, name)
        return function