import pygsheets
import json
from datetime import datetime


path1 = "D:/ResetEfficiency/"
gc_sheets = pygsheets.authorize(service_file=path1 + "credentials.json")

sheetname = 'evankae'
sh = gc_sheets.open(sheetname)
wks = sh[0]

nether_list = wks.get_col(col=5, include_tailing_empty=True, returnas='matrix')
nether_list.pop(0)
stronghold_list = wks.get_col(col=9, include_tailing_empty=True, returnas='matrix')
stronghold_list.pop(0)

nether_counter = 0
stronghold_counter = 0
nether_split_list = []

for i in range(len(nether_list)):
    if nether_list[i] != '':
        nether_counter += 1
    if stronghold_list[i] != '':
        stronghold_counter += 1
        nether_split_list.append("0" + str(datetime.strptime(stronghold_list[i], '%H:%M:%S') - datetime.strptime(nether_list[i], '%H:%M:%S')) + ".000")

conversion_rate = stronghold_counter/nether_counter
dict1 = {'conversion_rate': conversion_rate, 'distribution': nether_split_list}

with open(path1 + 'splitDist.json', 'w') as jsonFile:
    json.dump(dict1, jsonFile)
