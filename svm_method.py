#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import re
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, roc_curve, auc


batch = str(15)
data = pd.read_csv('./processed/%s_avg10_lowPower_data.csv' %batch)
X = data[['wind_speed', 'power']]
y = data['frozen']

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

model = SVC(kernel='rbf', C=1E10)
model.fit(X_test, y_test)
ymodel = model.predict(X_train)
print('验证集准确率：%0.3f\n\n'
    %accuracy_score(ymodel, y_train))