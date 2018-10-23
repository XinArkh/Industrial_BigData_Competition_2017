import csv
import re
from datetime import datetime

batch = str(21)  # 15 或 21

# 获取结冰时间，每个开始和结束时间作为一对数组存储在failureTime中
failureTime = []
with open('./%s/%s_failureInfo.csv' %(batch, batch), 'r') as failureInfo:
    failure = csv.reader(failureInfo)
    next(failure)
    for failure_row in failure:
        failureTime.append([datetime.strptime(failure_row[0], '%Y-%m-%d %H:%M:%S'),
            datetime.strptime(failure_row[1], '%Y-%m-%d %H:%M:%S')])

# 获取正常时间，每个开始和结束时间作为一对数组存储在normalTime中
normalTime = []
with open('./%s/%s_normalInfo.csv' %(batch, batch), 'r') as normalInfo:
    normal = csv.reader(normalInfo)
    next(normal)
    for normal_row in normal:
        normalTime.append([datetime.strptime(normal_row[0], '%Y-%m-%d %H:%M:%S'),
            datetime.strptime(normal_row[1], '%Y-%m-%d %H:%M:%S')])


with open('./%s/%s_data.csv' %(batch, batch), 'r') as read:
    reader = csv.reader(read)

    with open('./processed/%s_data.csv' %batch, 'w') as write:
        writer = csv.writer(write)
        titles = next(reader)
        titles.append('frozen')
        writer.writerow(titles)
        for data_row in reader:
            timepiece = datetime.strptime(data_row[0], '%Y-%m-%d %H:%M:%S')
            flag = 0
            for i in range(len(failureTime)):
                if failureTime[i][0] <= timepiece <= failureTime[i][1]:
                    data_row.append(1)
                    writer.writerow(data_row)
                    flag = 1
                    break
            if flag:    # 如果这一行已经属于结冰时间，被写入文件，就跳过这一轮
                continue
            for i in range(len(normalTime)):
                if normalTime[i][0] <= timepiece <= normalTime[i][1]:
                    data_row.append(0)
                    writer.writerow(data_row)
                    break