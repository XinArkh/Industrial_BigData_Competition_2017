import pickle
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix

batch = str(21)
# 数据集15与21互为训练集与测试集
modelNum = str(15) if batch == str(21) else str(21)

f=open('models/svm_model_%s.pkl' %modelNum,'rb')
model=pickle.load(f)

data = pd.read_csv('./processed/%s_avg10_lowPower_data.csv' %batch)
X = data[['wind_speed', 'power']]
y = data['frozen']

ypred = model.predict(X)
print('准确率：%0.3f' %accuracy_score(y, ypred))
# 评分公式：
# http://www.industrial-bigdata.com/competition/competitionAction!showDetail.action?competition.competitionId=1
tn, fp, fn, tp = confusion_matrix(y, ypred).ravel()
fault = len(y[y==1])
normal = len(y) - fault
alpha = fault / (fault + normal)
beta = 1 - alpha
print('得分：%0.3f' %(100*(1-alpha*fn/normal-beta*fp/fault)) )