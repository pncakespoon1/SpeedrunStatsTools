import pygsheets
import json
from datetime import datetime
from datetime import timedelta


path1 = "D:/ResetEfficiency/"
session_threshold = 1
jsonFile1 = open(path1 + "runners.json")
runners = json.load(jsonFile1)
gc_sheets = pygsheets.authorize(service_file=path1 + "credentials.json")
sheets = [{'name': 'semperzz3', 'start_row': 2, 'end_row': 75, 'version': 2},
          {'name': 'semperzz4', 'start_row': 274, 'end_row': 567, 'version': 3},
          {'name': 'semperzz4', 'start_row': 625, 'end_row': 676, 'version': 3},
          {'name': 'semperzz4', 'start_row': 773, 'end_row': 834, 'version': 3},
          {'name': 'semperzz4', 'start_row': 875, 'end_row': 907, 'version': 3},
          {'name': 'makattak112', 'start_row': 147, 'end_row': 291, 'version': 2},
          {'name': 'makattak112', 'start_row': 315, 'end_row': 361, 'version': 2},
          {'name': 'zylenox1', 'start_row': 5862, 'end_row': 8204, 'version': 1},
          {'name': 'zylenox1', 'start_row': 10544, 'end_row': 13044, 'version': 1},
          {'name': 'zylenox1', 'start_row': 13691, 'end_row': 16585, 'version': 1},
          {'name': 'zylenox1', 'start_row': 22398, 'end_row': 25556, 'version': 1}]


def get_sessions():
    sessions = []
    for runner in runners:
        for sheetname in runner['sheet_names']:
            print(sheetname)
            sh = gc_sheets.open(sheetname)
            wks = sh[1]
            headers = wks.get_row(row=1, returnas='matrix', include_tailing_empty=False)
            timestamps = wks.get_col(col=1, include_tailing_empty=False, returnas='matrix')
            timestamps.pop(0)
            bt_col = wks.get_col(col=headers.index("BT") + 1, returnas='matrix', include_tailing_empty=True)
            bt_col.pop(0)
            start_row = 2
            valid_session = False
            for i in range(len(timestamps) - 1):
                timestamp_1 = datetime.strptime(timestamps[i], '%Y-%m-%d %H:%M:%S')
                timestamp_2 = datetime.strptime(timestamps[i+1], '%Y-%m-%d %H:%M:%S')
                if bt_col[i] != '':
                    valid_session = True
                if timestamp_1 - timestamp_2 > timedelta(hours=session_threshold) or i == len(timestamps) - 2:
                    end_row = i + 2
                    if valid_session:
                        sessions.append({'name': sheetname, 'start_row': start_row, 'end_row': end_row, 'version': runner['tracker_versions'][runner['sheet_names'].index(sheetname)]})
                    start_row = i + 3
                    valid_session = False
    return sessions


def write_nether():
    sessions = get_sessions()
    print(sessions)
    nether_counter_1 = 0
    nether_counter_2 = 0
    stronghold_counter_1 = 0
    stronghold_counter_2 = 0
    split_list_1 = []
    split_list_2 = []
    for session in sessions:
        sh = gc_sheets.open(session['name'])
        wks = sh[1]
        headers = wks.get_row(row=1, returnas='matrix', include_tailing_empty=False)
        nether_col = wks.get_col(col=headers.index("Nether") + 1, include_tailing_empty=True, returnas='matrix')
        nether_col = nether_col[(session['start_row']-1):(session['end_row'])]
        if session['version'] == 1:
            stronghold_col = wks.get_col(col=headers.index("Eyes Crafted") + 1, include_tailing_empty=True, returnas='matrix')
        else:
            stronghold_col = wks.get_col(col=headers.index("Nether Exit") + 1, include_tailing_empty=True, returnas='matrix')
        stronghold_col = stronghold_col[(session['start_row']-1):(session['end_row'])]
        label_col = wks.get_col(col=headers.index("BT") + 1, include_tailing_empty=True, returnas='matrix')
        label_col = label_col[(session['start_row']-1):(session['end_row'])]

        for i in range(len(nether_col)):
            if nether_col[i] != '':
                if label_col[i] != '':
                    nether_counter_1 += 1
                    if stronghold_col[i] != '':
                        stronghold_counter_1 += 1
                        split_list_1.append("0" + str(datetime.strptime(stronghold_col[i], '%H:%M:%S') - datetime.strptime(nether_col[i], '%H:%M:%S')) + ".000")
                else:
                    nether_counter_2 += 1
                    if stronghold_col[i] != '':
                        stronghold_counter_2 += 1
                        split_list_2.append("0" + str(datetime.strptime(stronghold_col[i], '%H:%M:%S') - datetime.strptime(nether_col[i], '%H:%M:%S')) + ".000")

    conversion_rate_1 = stronghold_counter_1/nether_counter_1
    dict1 = {'conversion_rate': conversion_rate_1, 'distribution': split_list_1}
    print(dict1)
    with open(path1 + 'nether_dist1.json', 'w') as jsonFile1:
        #json.dump(dict1, jsonFile1)
        jsonFile1.close()

    conversion_rate_2 = stronghold_counter_2/nether_counter_2
    dict2 = {'conversion_rate': conversion_rate_2, 'distribution': split_list_2}
    print(dict2)
    with open(path1 + 'nether_dist2.json', 'w') as jsonFile2:
        #json.dump(dict2, jsonFile2)
        jsonFile2.close()


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

write_nether()