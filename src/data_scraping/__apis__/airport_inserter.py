from openpyxl import load_workbook
from os import path
from time import sleep, time
from src.data_scraping.__apis__.inserter import Inserter


start = time()
print("Loading data...")
sleep(1)
data = path.abspath(path.join('..', '..', '..', 'data'))

book = load_workbook(path.join(data, 'airports.xlsx'))
sheet = book['1']

print("Connecting...")
sleep(1)
ins = Inserter(data)

print("Preparing database...")
ins.prepare_command("""PREPARE airport_insert AS 
    INSERT INTO public."Airport" VALUES ($1, $2, $3)""")

print('Executing Insert...')
i = 0
sleep(2)
for row in sheet.rows:
    i += ins.execute_command('airport_insert', (str(row[0].value), str(row[1].value), str(row[2].value)))

end = time()
ins.close()
print("{} rows inserted".format(i))
print("Time elapsed: {}m:{}s".format(int(round((end-start)/60, 0)), int(round((end-start)%60, 0))))