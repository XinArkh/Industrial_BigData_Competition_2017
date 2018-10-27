import re
import csv
import numpy as np
import pandas as pd

batch = str(21)  # 15 或 21

data = pd.read_csv('./processed/%s_data.csv' %batch)
with open('./processed/%s_avg10_data.csv' %batch, 'w') as write:
    writer = csv.writer(write)
    titles = data.columns
    writer.writerow(titles)

    length = len(data)
    minutes = 10  # time period (minutes) to be averaged # 5 or 10
    i = 0
    j = 1
    while i + j < length:
        Y, MON, D, H, M = [int(item) for item in re.split('-| |:', data['time'][i])[:5]]
        MTIME = (M + minutes) if (M + minutes < 60) else (M + minutes - 60)
        while i + j < length:
            y, mon, d, h, m = [int(item) for item in re.split('-| |:', data['time'][i+j])[:5]]
            if m >= MTIME or h > H or d > D or mon > MON or y > Y:
                break
            j += 1
        outputLine = []
        outputLine.append(data['time'][i])
        for k in range(1, len(titles[1:-1])+1):
            outputLine.append(data[titles[k]][i:i+j].mean())
        flag = 1 if np.any(data['frozen'][i:i+j]) else 0
        outputLine.append(flag)
        writer.writerow(outputLine)
        i += j
        j = 1