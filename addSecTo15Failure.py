'''
    在15_failureInfo_raw.csv开始时间与结束时间的时间戳最后添加秒数据
    注意：此脚本已作废，不需要运行
'''

import csv

with open('./15/15_failureInfo_raw.csv', 'r') as read:
    reader = csv.reader(read)

    with open('./15/15_failureInfo.csv', 'w') as write:
        writer = csv.writer(write)
        writer.writerow(next(reader))
        for read_row in reader:
            read_row[0] = read_row[0] + ':00'
            read_row[1] = read_row[1] + ':59'
            writer.writerow(read_row)