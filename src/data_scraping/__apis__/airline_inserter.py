import openpyxl
import os
import psycopg2
from src.data_scraping.__apis__.inserter import Inserter
import time





start = time.time()
print("Loading data...")
time.sleep(1)
data = os.path.abspath(os.path.join('..', '..', '..', 'data'))

book = openpyxl.load_workbook(os.path.join(data, 'airlines.xlsx'))
sheet = book['airlines']

print("Connecting...")
ins = Inserter(data)
time.sleep(1)

print("Preparing database...")
time.sleep(2)
ins.prepare_command("""PREPARE airline_insert AS 
    INSERT INTO airline VALUES ($1, $2)""")


print('Executing Insert...')
time.sleep(2)
i = 0
for row in sheet.rows:
    i += ins.execute_command('airline_insert', (str(row[0].value), str(row[1].value)))

end = time.time()
ins.close()
print("{} rows inserted".format(i))
print("Time elapsed: {}m:{}s".format(int(round((end-start)/60, 0)), int(round((end-start)%60, 0))))