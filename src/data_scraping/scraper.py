import os, time

from src.data_scraping.__apis__.qpx import QPX
from src.data_scraping.__apis__.db_writer import DB


if __name__ == '__main__':
    data_path = os.path.abspath(os.path.join(os.getcwd(), "..", "..", "data"))
    trip_routes = os.path.join(data_path, 'TripRoutes.json')
    tomorrow = 60 * 60 * 24

    flight_api = QPX(data_path)
    db = DB(data_path)
    start = time.time()
    trip_list = list()
    i = 3
    with open(os.path.join(data_path, '{}.txt'.format(i))) as file:
        for line in file.readlines():
            print(line)
            args = line.split(',')
            trip_list.append(flight_api.make_request(args[0], args[1], args[2]))
    db.insert_trip_data(trip_list)

    elapsed = time.time() - start
    m,s = divmod(elapsed, 60)
    h,m = divmod(m, 60)
    with open('data.txt','a+') as file:
        file.write("Time taken to insert 100 rows: {}h{}m{}s\n".format(int(h), int(m), int(s)))
