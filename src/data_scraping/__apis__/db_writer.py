import json
import os
import psycopg2


class DB:
    def __init__(self, data_path):
        self._url = (self._get_db_url(data_path))
        self._get_root_login(data_path)
        print(self._url[0], self._db_user, self._db_password)
        self.conn = psycopg2.connect(user=self._db_user, password=self._db_password, host=self._url[0], dbname='flights')

    def _get_db_url(self, data_path):
        file_location = os.path.join(data_path, 'db_url.json')
        with open(file_location) as data_file:
            json_file = json.load(data_file)
            return json_file['url'], json_file['port']

    def _get_root_login(self, data_path):
        file_location = os.path.join(data_path, 'db_login.json')
        with open(file_location) as data_file:
            json_file = json.load(data_file)
            self._db_password = json_file['password']
            self._db_user = json_file['user']

    def get_connection(self):
        return self.conn
