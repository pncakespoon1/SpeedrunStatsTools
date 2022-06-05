import matplotlib.colors
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pygsheets
import json
from datetime import timedelta
from datetime import datetime
import math
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap


path1 = "D:/ResetEfficiency/"
gc_sheets = pygsheets.authorize(service_file=path1 + "credentials.json")

jsonFile1 = open(path1 + "runners.json")
runners = json.load(jsonFile1)
jsonFile2 = open(path1 + 'effscore_keys.json')
effscore_keys = json.load(jsonFile2)
scatterplot1_color_palette = {0: (0, 1, 0)}
target_time = 600


def get_sheet(sheetname):
    sh = gc_sheets.open(sheetname)
    wks = sh[1]
    return wks


def get_distribution(sheetname, colname):
    wks = get_sheet(sheetname)
    headers = wks.get_row(row=0, returnas='matrix', include_tailing_empty=False)
    column = wks.get_col(col=headers.index(colname) + 1, returnas='matrix', include_tailing_empty=False)
    column.pop(0)
    for cell in column:
        if cell == '':
            column.remove('')
    return column


def hue_dict():
    dict = {1000: (0, 0, 1)}
    for i in range(0, 293):
        dict = dict | {float(i): (round((-0.95 * (0.991 ** i) + 0.95), 3), 0, 0)}
    return dict


def get_stats(sheetname, uses_spec_tracker):
    one_hour = timedelta(hours=1)
    wks = get_sheet(sheetname)
    headers = wks.get_row(row=1, returnas='matrix', include_tailing_empty=False)
    nether_col = wks.get_col(col=headers.index("Nether") + 1, returnas='matrix', include_tailing_empty=True)
    nether_col.pop(0)
    rta_col = wks.get_col(col=headers.index("RTA") + 1, returnas='matrix', include_tailing_empty=True)
    rta_col.pop(0)
    if uses_spec_tracker:
        rta_since_prev_col = wks.get_col(col=headers.index("RTA Since Prev") + 1, returnas='matrix', include_tailing_empty=True)
        rta_since_prev_col.pop(0)
    nether_count = 0
    entry_sum = timedelta(seconds=0)
    rta_sum = timedelta(seconds=0)
    for i in range(len(nether_col)):
        nether_cell = nether_col[i]
        rta_cell = rta_col[i]
        rta_cell = timedelta(hours=int(rta_cell[0:1]), minutes=int(rta_cell[2:4]), seconds=int(rta_cell[5:7]))
        if uses_spec_tracker:
            rta_since_prev_cell = rta_since_prev_col[i]
            rta_since_prev_cell = timedelta(hours=int(rta_since_prev_cell[0:1]), minutes=int(rta_since_prev_cell[2:4]), seconds=int(rta_since_prev_cell[5:7]))
            rta_sum += (rta_cell + rta_since_prev_cell)
        else:
            rta_sum += rta_cell
        if nether_cell != '':
            nether_cell = timedelta(hours=int(nether_cell[0:1]), minutes=int(nether_cell[2:4]), seconds=int(nether_cell[5:7]))
            nether_count += 1
            entry_sum += nether_cell
            rta_sum -= (rta_cell - nether_cell)
    hours = rta_sum / one_hour
    nph = nether_count / hours
    avgEnter = entry_sum / nether_count
    return nph, avgEnter

def makeplots():
    nph_list = []
    avgEnter_list = []
    sheetname_list = []
    hue_list = []
    size_list = []

    for x in range(60, 140):
        for y in range(90, 150):
            y = y/1
            effscore = (x/10) * effscore_keys[1][effscore_keys[0].index(5*(math.floor((target_time - y)/5)))]
            nph_list.append(x/10)
            avgEnter_list.append(y)
            hue_list.append(round(effscore * 10000))
            size_list.append(1)
    for runner in runners:
        for i in range(len(runner['sheet_names'])):
            uses_spec_tracker = True
            if runner['tracker_versions'][i] == 1:
                uses_spec_tracker = False
            nph, avgEnter = get_stats(runner['sheet_names'][i], uses_spec_tracker)
            avgEnter = avgEnter / timedelta(seconds=1)
            nph_list.append(nph)
            avgEnter_list.append(avgEnter)
            sheetname_list.append(runner['sheet_names'][i])
            hue_list.append(1000)
            size_list.append(3)

    dict1 = {'nph': nph_list, 'avgEnter': avgEnter_list, 'hues': hue_list, 'sheetnames': sheetname_list}
    huedict = hue_dict()

    sns.scatterplot(x='nph', y='avgEnter', hue='hues', palette=huedict, data=dict1, legend=False, sizes=size_list)
    plt.savefig(path1 + 'figures/plot.png', dpi=1000)

makeplots()
