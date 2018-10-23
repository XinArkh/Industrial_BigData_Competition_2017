# import tensorflow as tf
import numpy as np
import csv
from datetime import datetime

with open(r'C:\Users\Yuhang Du\Desktop\ACT\python\21\Ldata_21.csv', 'w', newline='') as Ldata:
    writer = csv.writer(Ldata)
    with open(r'C:\Users\Yuhang Du\Desktop\ACT\python\21\21_data.csv', 'r+') as data:
        reader = csv.reader(data)
        next(reader)                # skip the first line
        with open(r'C:\Users\Yuhang Du\Desktop\ACT\python\21\21_failureInfo.csv', 'r+') as failureInfo:
            failure = csv.reader(failureInfo)
            next(failure)
            # failure状态数组初始化
            failure_time_start = []
            failure_time_end = []
            for failure_row in failure:
                failure_time_start.append(datetime.strptime(failure_row[0], '%Y-%m-%d %H:%M:%S'))
                failure_time_end.append(datetime.strptime(failure_row[1], '%Y-%m-%d %H:%M:%S'))
            with open(r'C:\Users\Yuhang Du\Desktop\ACT\python\21\21_normalInfo.csv', 'r+') as normalInfo:
                normal = csv.reader(normalInfo)
                next(normal)
                # normal状态数组初始化
                normal_time_start = []
                normal_time_end = []
                for normal_row in normal:
                    normal_time_start.append(datetime.strptime(normal_row[0], '%Y-%m-%d %H:%M:%S'))
                    normal_time_end.append(datetime.strptime(normal_row[1], '%Y-%m-%d %H:%M:%S'))

                # 判断21_data文件是否为第一行（表头）
                first_row = 1
                # 进入21_data文件读取数据判断每一行的时间戳是什么Lable:如果异常为1，正常为0，未出现为-1
                for data_row in reader:
                    if first_row == 1:
                        first_row = 0
                        continue

                    flag = 0
                    data_time = datetime.strptime(data_row[0], '%Y-%m-%d %H:%M:%S')
                    # 判断当前时间戳是否在某个故障时间段内
                    for i in range(len(failure_time_start)):
                        if failure_time_start[i] <= data_time <= failure_time_end[i]:
                            data_row.append(1)
                            writer.writerow(data_row)
                            flag = 1
                            break
                    # 如果是（故障时间），就将当前行数据写入Ldata.csv文件中，结束循环，继续标识下一行数据
                    if flag == 1:
                        continue
                    # 判断当前时间戳是否在某个正常时间段内
                    for i in range(len(normal_time_start)):
                        if normal_time_start[i] <= data_time <= normal_time_end[i]:
                            data_row.append(0)
                            writer.writerow(data_row)
                            flag = 1
                            break
                    # 如果是（正常时间），就将当前行数据写入Ldata.csv文件中，结束循环，继续标识下一行数据
                    if flag == 1:
                        continue
                    # 如果既不是异常状态又不是正常状态，就将Lable置为-1
                    else:
                        # data_row.append(-1)
                        # writer.writerow(data_row)
                        pass