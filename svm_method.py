#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# pickle写入方法：
# 1. pickle.dump()
#
# with open('test.txt', 'wb') as f:
#     pickle.dump(sth, f)
#
# 2. pickle.dumps()
#
# s = pickle.dumps(sth)
# with open('test.txt', 'wb') as f:
#     f.write(s)

# 可优化方向：
# 1. 数据归一化处理(done)
# 2. 网格搜索寻找SVM最优参数(C&gamma)
# 3. 绘制roc曲线以评价模型

import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_curve, auc


def _Train_Test_Gen(X, y, method='normal', train_size=5000, random_state=1):
    if method == 'normal':
        return train_test_split(X, y, train_size=5000, random_state=1)
    elif method == 'RandomOverSampling':
        # 打乱数据顺序
        index = np.arange(len(y))
        np.random.shuffle(index)
        X = X.reindex(index)
        y = y.reindex(index)
        # 根据有无结冰拆分数据
        X_1 = X[y>0]
        y_1 = y[y>0]
        X_0 = X[y==0]
        y_0 = y[y==0]
        # 结冰与不结冰各自拆分训练集与验证集,结冰训练集取1000个（然后复制一倍），不结冰取3000个
            # 结冰部分
        X_1_train = pd.concat([X_1[:1000], X_1[:1000]], ignore_index=True)
        y_1_train = pd.concat([y_1[:1000], y_1[:1000]], ignore_index=True)
        X_1_test = X_1[1000:]
        y_1_test = y_1[1000:]
            # 不结冰部分
        X_0_train = X_0[:3000]
        y_0_train = y_0[:3000]
        X_0_test = X_0[3000:]
        y_0_test = y_0[3000:]
        # 合并有/无结冰数据的训练集/验证集
        X_train = pd.concat([X_1_train, X_0_train], ignore_index=True)
        y_train = pd.concat([y_1_train, y_0_train], ignore_index=True)
        X_test = pd.concat([X_1_test, X_0_test], ignore_index=True)
        y_test = pd.concat([y_1_test, y_0_test], ignore_index=True)
        return [X_train, X_test, y_train, y_test]


# batch-训练集；minutes-平均分钟数；elementList-所选特征；norm-是否归一化处理
def SVM_Method(batch, minutes, elementList, norm, roc=True):
    # 效果较好的特征有：wind_speed与power；pitch%NUM%_angle与power；
    # pitch%NUM%_speed与power；yaw_speed与power；
    # pitch1_ng5_DC，pitch2_ng5_DC，pitch3_ng5_DC与power
    elementList = sorted(elementList)

    data = pd.read_csv('./processed/%s_avg%s_lowPower_data.csv' %(batch, str(minutes)))
    X = data[elementList]
    C = pd.read_csv('./processed/%s_avg%s_C.csv' %(batch, str(minutes)))
    C[X['wind_speed']<0.175] = 0
    X = pd.concat([X, C], axis=1)
    if norm:
        X_min = X.min()
        X_max = X.max()
        X = (X - X_min) / (X_max - X_min)
    y = data['frozen']

    X_train, X_test, y_train, y_test = _Train_Test_Gen(X, y, method='RandomOverSampling', train_size=5000, random_state=1)

    model = SVC(kernel='rbf', C=1E10)
    model.fit(X_train, y_train)
    ymodel = model.predict(X_test)
    print('验证集准确率：%0.3f\n\n' %accuracy_score(ymodel, y_test))

    if norm:
        with open('models/svm_model_%s_norm+%s.pkl' %(batch, '+'.join(elementList)), 'wb') as f:
            pickle.dump([model, [X_min, X_max]], f)
    else:
        with open('models/svm_model_%s+%s.pkl' %(batch, '+'.join(elementList)), 'wb') as f:
            pickle.dump(model, f)

    # drawing ROC curve
    if roc:
        yscore = model.decision_function(X_test)
        fpr, tpr, _ = roc_curve(y_test, yscore)
        roc_auc = auc(fpr, tpr)

        plt.figure()
        lw = 2
        plt.plot(fpr, tpr, color='darkorange',
                 lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)
        plt.plot([0, 1], [0, 1], '--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.005])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curve of the Model')
        plt.legend(loc="lower right")
        plt.show()



if __name__ == '__main__':
    SVM_Method(batch=str(15), minutes=1, 
        elementList=['wind_speed', 'pitch1_angle', 'pitch1_speed', 'power'], norm=True)