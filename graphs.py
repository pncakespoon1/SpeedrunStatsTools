import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pygsheets
import json


path1 = "D:/ResetEfficiency/"
gc_sheets = pygsheets.authorize(service_file=path1 + "credentials.json")

jsonFile = open(path1 + "runners.json")
runners = json.load(jsonFile)


def get_sheet(sheetname):
    sh = gc_sheets.open(sheetname)
    wks = sh[1]
    return wks


def get_distribution(sheetname, colname):
    wks = get_sheet(sheetname)
    headers = wks.get_row(row=0, returnas='matrix', include_tailing_empty=False)
    column = wks.get_col(col=headers.index(colname), returnas='matrix', include_tailing_empty=False)
    column.pop(0)
    for cell in column:
        if cell == '':
            column.remove('')
    return column
