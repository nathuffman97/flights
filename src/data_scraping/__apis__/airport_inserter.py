import openpyxl
import os
import psycopg2
import json
import time
from src.data_scraping.__apis__.inserter import Inserter


start = time.time()
print("Loading data...")
time.sleep(1)
data = os.path.abspath(os.path.join('..', '..', '..', 'data'))

book = openpyxl.load_workbook(os.path.join(data, 'airports.xlsx'))
sheet = book['1']


print("Connecting...")
time.sleep(1)
ins = Inserter(data)

print("Preparing database...")
ins.prepare_command("""PREPARE airport_insert AS 
    INSERT INTO airport VALUES ($1, $2, $3)""")

print('Executing Insert...')
time.sleep(2)
for row in sheet.rows:
    ins.execute_command('airport_insert', (str(row[0].value), str(row[1].value), str(row[2].value)))

end = time.time()
ins.close()
print("Time elapsed: {}m:{}s".format(round((end-start)/60, 0), round((end-start)%60, 0)))