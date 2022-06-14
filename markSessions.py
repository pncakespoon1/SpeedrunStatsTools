import gspread
import json
import datetime
from datetime import datetime
from datetime import timedelta
import re


def convert_to_datetime(string):
    print(string)
    string = re.sub('/', '$', string, count=1)
    string = re.sub(':', '&', string, count=1)
    month = int(string[0:(string.index('$'))])
    day = int(string[(string.index('$')+1):(string.index('/'))])
    year = int(string[(string.index('/')+1):(string.index(' '))])
    hour = int(string[(string.index(' ')+1):(string.index('&'))])
    minute = int(string[(string.index('&')+1):(string.index(':'))])
    second = int(string[(string.index(':')+1):])
    time = datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
    return time


#settings_file = open("settings.json")
#settings = json.load(settings_file)
#settings_file.close()
gc = gspread.service_account(filename="D:/ResetEfficiency/credentials.json")
#sh = gc.open_by_url(settings['spreadsheet-link'])
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1wWgTf5I-Ik8ZtahTqlahLN1CL5sD3_iGat7P10NYBZ4/edit#gid=1760430564')
dataSheet = sh.worksheet('Raw Data')
rows = dataSheet.get_all_values()
new_session_rows = []
min_row = 1
for i in range(len(rows)):
    if rows[i][len(rows[i])-1] == 'X':
        min_row = i
for i in range(min_row+1, len(rows)-1):
    print(rows[i][0])
    time1 = convert_to_datetime(rows[i][0])
    time2 = convert_to_datetime(rows[i+1][0])
    if time1 - time2 > timedelta(hours=6):
        new_session_rows.append(i+1)
    if i + 2 == len(rows):
        new_session_rows.append(i+2)
print(new_session_rows)
for row_num in new_session_rows:
    dataSheet.update_cell(row_num, len(rows[0]), "X")
