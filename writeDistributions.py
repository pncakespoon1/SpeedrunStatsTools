import pygsheets
import json
from datetime import datetime


path1 = "D:/ResetEfficiency/"
gc_sheets = pygsheets.authorize(service_file=path1 + "credentials.json")


sh = gc_sheets.open('evankae')
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
        nether_split_list.append(datetime.strptime(stronghold_list[i], '%H:%M:%S') - datetime.strptime(nether_list[i], '%H:%M:%S'))


