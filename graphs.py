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


