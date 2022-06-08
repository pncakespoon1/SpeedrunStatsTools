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
import random
from matplotlib import axes
from matplotlib import transforms
import scipy


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


def get_stats(sheetname, tracker_version):
    print(sheetname)
    entry_dist = []
    randomized_entry_dist = []
    entry_labels = []
    randomized_entry_labels = []
    one_hour = timedelta(hours=1)
    wks = get_sheet(sheetname)
    headers = wks.get_row(row=1, returnas='matrix', include_tailing_empty=False)
    nether_col = wks.get_col(col=headers.index("Nether") + 1, returnas='matrix', include_tailing_empty=True)
    nether_col.pop(0)
    rta_col = wks.get_col(col=headers.index("RTA") + 1, returnas='matrix', include_tailing_empty=True)
    rta_col.pop(0)
    bt_col = wks.get_col(col=headers.index("BT") + 1, returnas='matrix', include_tailing_empty=True)
    bt_col.pop(0)
    shipwreck_col = wks.get_col(col=headers.index("shipwreck") + 1, returnas='matrix', include_tailing_empty=True)
    shipwreck_col.pop(0)
    if tracker_version in [2, 3]:
        rta_since_prev_col = wks.get_col(col=headers.index("RTA Since Prev") + 1, returnas='matrix', include_tailing_empty=True)
        rta_since_prev_col.pop(0)
    nether_count = 0
    entry_sum = timedelta(seconds=0)
    rta_sum = timedelta(seconds=0)
    for i in range(len(nether_col)):
        nether_cell = nether_col[i]
        rta_cell = rta_col[i]
        rta_cell = timedelta(hours=int(rta_cell[0:1]), minutes=int(rta_cell[2:4]), seconds=int(rta_cell[5:7]))
        if tracker_version in [2, 3]:
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
            entry_dist.append((nether_cell) / timedelta(seconds=1))
            if bt_col[i] != '':
                entry_labels.append('bt')
            elif shipwreck_col[i] != '':
                entry_labels.append('shipwreck')
            else:
                entry_labels.append('other')

    hours = rta_sum / one_hour
    nph = nether_count / hours
    avgEnter = entry_sum / nether_count
    avgEnter = avgEnter / timedelta(seconds=1)
    for i in range(10000):
        index = random.randrange(0, len(entry_dist))
        randomized_entry_dist.append(entry_dist[index])
        randomized_entry_labels.append(entry_labels[index])
    return nph, avgEnter, randomized_entry_dist, randomized_entry_labels


def make_scatterplot1(nph_list, avgEnter_list, sheetname_list):
    canvas = []
    for x in range(60, 140):
        canvas.append([])
        for y in range(90, 150):
            y = y / 1
            effscore = (x / 10) * effscore_keys[1][effscore_keys[0].index(5 * (math.floor((target_time - y) / 5)))]
            (canvas[x - 60]).append(effscore)

    dict1 = {'nph': nph_list, 'avgEnter': avgEnter_list, 'sheetname': sheetname_list}

    x1 = np.linspace(6, 14.0, 60)
    x2 = np.linspace(90, 150, 80)
    x, y = np.meshgrid(x1, x2)
    cm = plt.cm.get_cmap('cividis')
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    p1 = plt.contourf(x, y, canvas, levels=1000)
    p2 = sns.scatterplot(x='nph', y='avgEnter', data=dict1, legend=False)
    plt.savefig(path1 + 'figures/plot1.png', dpi=1000)
    plt.close()


def make_histogram1(entry_dist_list):
    count = 0
    for runner in runners:
        runner_name = runner['twitch_name']
        print(runner_name)
        entry_dists_flattened = []
        entry_dists_flat_labels = []
        for sheetname in range(len(runner['sheet_names'])):
            for item in entry_dist_list[count]:
                if 7 < item < 210:
                    entry_dists_flattened.append(item)
                    entry_dists_flat_labels.append(sheetname)
            count += 1

        dict1 = {'entry_dist': entry_dists_flattened, 'sheetname': entry_dists_flat_labels}

        sns.kdeplot(data=dict1, x='entry_dist', hue='sheetname', legend=False, bw_adjust=0.9)
        plt.savefig(path1 + f'figures/histogram1_{runner_name}.png', dpi=1000)
        plt.close()


def make_histogram2(entry_dist_list, entry_labels_list):
    count = 0
    for runner in runners:
        for sheetname in runner['sheet_names']:
            entry_dist = []
            entry_labels = []
            for i in range(len(entry_dist_list[count])):
                if 7 < entry_dist_list[count][i] < 210:
                    entry_dist.append(entry_dist_list[count][i])
                    entry_labels.append(entry_labels_list[count][i])

            count += 1
            dict1 = {'entry_dist': entry_dist, 'sheetname': entry_labels}

            sns.kdeplot(data=dict1, x='entry_dist', hue='sheetname', legend=False, bw_adjust=0.9)
            plt.savefig(path1 + f'figures/histogram1_{sheetname}.png', dpi=1000)
            plt.close()


def makeplots(scatterplot1, histogram1):
    nph_list = []
    avgEnter_list = []
    entry_dist_list = []
    entry_labels_list = []
    sheetname_list = []

    for runner in runners:
        for i in range(len(runner['sheet_names'])):
            nph, avgEnter, entry_dist, entry_labels = get_stats(runner['sheet_names'][i], runner['tracker_versions'][i])
            nph_list.append(nph)
            avgEnter_list.append(avgEnter)
            entry_dist_list.append(entry_dist)
            entry_labels_list.append(entry_labels)
            sheetname_list.append(runner['sheet_names'][i])

    if scatterplot1:
        make_scatterplot1(nph_list, avgEnter_list, sheetname_list)

    if histogram1:
        make_histogram1(entry_dist_list)


makeplots(False, False)
