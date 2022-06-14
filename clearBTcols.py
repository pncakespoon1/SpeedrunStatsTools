import pygsheets
import json
import numpy as np

path1 = "D:/ResetEfficiency/"
jsonFile1 = open(path1 + "runners.json")
runners = json.load(jsonFile1)
gc_sheets = pygsheets.authorize(service_file=path1 + "credentials.json")

for runner in runners:
    for i in range(len(runner['sheet_names'])):
        sheetname = runner['sheet_names'][i]
        print(sheetname)
        tracker_version = runner['tracker_versions'][i]
        sh = gc_sheets.open(sheetname)
        wks = sh[1]
        col_label = 'AL'
        if tracker_version == 2:
            col_label = 'AO'
        if tracker_version == 3:
            col_label = 'AE'
        headers = wks.get_row(row=1, returnas='matrix', include_tailing_empty=False)
        wks.clear(start=col_label + '2', end=col_label + str(len(wks.get_col(col=headers.index('BT')+1, returnas='matrix', include_tailing_empty=True))))
