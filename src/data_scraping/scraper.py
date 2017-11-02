import os, time

from src.data_scraping.__apis__.qpx import QPX
from src.data_scraping.__apis__.db_writer import DB


if __name__ == '__main__':
    data_path = os.path.abspath(os.path.join(os.getcwd(), "..", "..", "data"))
    trip_routes = os.path.join(data_path, 'TripRoutes.json')
    tomorrow = 60 * 60 * 24

    flight_api = QPX(data_path)
    db = DB(data_path)
    i = 0
    while i < 3:
        i += 1
        start = time.time()
        with open(os.path.join(data_path, '{}.txt'.format(i))) as file:
            for line in file:
                print(line)
                line = file.readline()
                args = line.split(',')
                result_list = flight_api.make_request(args[0], args[1], args[2])
                for result in result_list:
                    db.insert_trip_data(result)
        elapsed = time.time() - start
        m,s = divmod(elapsed, 60)
        h,m = divmod(m, 60)
        open('data.txt','a+').write("Time taken to insert 100 rows: {}h{}m{}s\n".format(int(h), int(m), int(s)))
