#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
from sklearn.metrics import accuracy_score, confusion_matrix


def Score(batch, minutes, elementList, norm):
    elementList = sorted(elementList)

    # 数据集15与21互为训练集与测试集
    testBatch = str(15) if batch == str(21) else str(21)
    if norm:
        f = open('models/svm_model_%s_norm+%s.pkl' %(batch, '+'.join(elementList)), 'rb')
        model, [X_min, X_max] = pickle.load(f)
    else:
        f = open('models/svm_model_%s+%s.pkl' %(batch, '+'.join(elementList)), 'rb')
        model = pickle.load(f)

    data = pd.read_csv('./processed/%s_avg%s_lowPower_data.csv' %(testBatch, str(minutes)))
    X = data[elementList]
    C = pd.read_csv('./processed/%s_avg%s_C.csv' %(testBatch, str(minutes)))
    C[X['wind_speed']<0.175] = 0
    X = pd.concat([X, C], axis=1)
    if norm:
        X = (X - X_min) / (X_max - X_min)
    y = data['frozen']

    ypred = model.predict(X)
    print('准确率：%0.2f%%' %(accuracy_score(y, ypred) * 100))
    # 评分公式：
    # http://www.industrial-bigdata.com/competition/competitionAction!showDetail.action?competition.competitionId=1
    # 注意这里的p和n与公式中是相反的
    tn, fp, fn, tp = confusion_matrix(y, ypred).ravel()
    # print([tn, fp, fn, tp])
    fullData = pd.read_csv('./processed/%s_avg%s_data.csv' %(testBatch, str(minutes)))
    highPower = fullData.loc[fullData['power'] >= 2]
    highY = highPower['frozen']
    fn += len(highY[highY==1])
    tn += len(highY[highY==0])

    fault = len(y[y==1]) + len(highY[highY==1])
    normal = len(y) + len(highY) - fault
    alpha = fault / ( fault + normal )
    beta = 1 - alpha
    print('得分：%0.3f' %(100*(1-alpha*fp/normal-beta*fn/fault)))

    sns.heatmap([[tn, fp], [fn, tp]], annot=True, fmt='d', cbar=False, 
        xticklabels=['0', '1'], yticklabels=['0', '1'])
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.show()


if __name__ == '__main__':
    Score(batch=str(15), minutes=1, 
        elementList=['wind_speed', 'pitch1_angle', 'pitch1_speed', 'power'], norm=True)