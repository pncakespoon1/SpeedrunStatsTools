import pygsheets
import json
from datetime import datetime
from datetime import timedelta

path1 = "D:/ResetEfficiency/"
gc_sheets = pygsheets.authorize(service_file=path1 + "credentials.json")



def write_netherToStronghold():
    sheetname = 'evankae'
    sh = gc_sheets.open(sheetname)
    wks = sh[0]
    nether_list = wks.get_col(col=5, include_tailing_empty=True, returnas='matrix')
    nether_list.pop(0)
    stronghold_list = wks.get_col(col=9, include_tailing_empty=True, returnas='matrix')
    stronghold_list.pop(0)

    nether_counter = 0
    stronghold_counter = 0
    split_list = []

    for i in range(len(nether_list)):
        if nether_list[i] != '':
            nether_counter += 1
        if stronghold_list[i] != '':
            stronghold_counter += 1
            split_list.append("0" + str(datetime.strptime(stronghold_list[i], '%H:%M:%S') - datetime.strptime(nether_list[i], '%H:%M:%S')) + ".000")

    conversion_rate = stronghold_counter/nether_counter
    dict1 = {'conversion_rate': conversion_rate, 'distribution': split_list}

    with open(path1 + 'splitDist1.json', 'w') as jsonFile:
        json.dump(dict1, jsonFile)


def write_endFight():
    sheetname = 'endfightdistribution'
    sh = gc_sheets.open(sheetname)
    wks = sh[2]
    split_list = []
    values = wks.get_col(col=1, returnas='matrix', include_tailing_empty=False)
    frequencies = wks.get_col(col=2, returnas='matrix', include_tailing_empty=False)
    for value_num in range(len(values)):
        if int(frequencies[value_num]) > 0:
            for i in range(int(frequencies[value_num])):
                split_list.append("0" + str(timedelta(seconds=int(values[value_num]))) + ".000")
    dict1 = {'conversion_rate': 0.975, 'distribution': split_list}
    with open(path1 + 'splitDist2.json', 'w') as jsonFile:
        json.dump(dict1, jsonFile)

write_endFight()