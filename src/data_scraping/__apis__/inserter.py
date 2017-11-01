import psycopg2
import json
from os import path


class Inserter():

    def __init__(self, path):
        _url = self._get_db_url(path)
        password, login = self._get_root_login(path)
        self.conn = psycopg2.connect(host=_url, dbname='flights', user=login, password=password)
        self.cur = self.conn.cursor()

    def _get_db_url(self, data_path):
        file_location = path.join(data_path, 'db_url.json')
        with open(file_location) as data_file:
            json_file = json.load(data_file)
            return json_file['url']

    def _get_root_login(self, data_path):
        file_location = path.join(data_path, 'db_login.json')
        with open(file_location) as data_file:
            json_file = json.load(data_file)
            return json_file['password'], json_file['user']

    def prepare_command(self, command):
        try:
            self.cur.execute(command)
        except psycopg2.ProgrammingError as e:
            self.conn.rollback()

    def execute_command(self, name, args):
        try:
            self.cur.execute("EXECUTE {} ({}{})".format(name, '%s, '*(len(args)-1), '%s'), args)
        except psycopg2.Error as e:
            self.conn.rollback()
            return 0
        else:
            self.conn.commit()
            return 1

    def close(self):
        self.cur.close()
        self.conn.close()