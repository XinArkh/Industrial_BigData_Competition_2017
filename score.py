import pickle
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix

# 测试数据集，15或21
batch = str(21)
elementList = sorted(['wind_speed', 'pitch1_angle', 'pitch1_speed', 'power'])
norm = True

# 数据集15与21互为训练集与测试集
modelNum = str(15) if batch == str(21) else str(21)
if norm:
    f = open('models/svm_model_%s_norm+%s.pkl' %(modelNum, '+'.join(elementList)), 'rb')
    model, [_means, _stds] = pickle.load(f)
else:
    f = open('models/svm_model_%s+%s.pkl' %(modelNum, '+'.join(elementList)), 'rb')
    model = pickle.load(f)

data = pd.read_csv('./processed/%s_avg30_lowPower_data.csv' %batch)
X = data[elementList]
if norm:
    X = (X - _means) / _stds
y = data['frozen']

ypred = model.predict(X)
print('准确率：%0.3f' %accuracy_score(y, ypred))
# 评分公式：
# http://www.industrial-bigdata.com/competition/competitionAction!showDetail.action?competition.competitionId=1
# 注意这里的p和n与公式中是相反的
tn, fp, fn, tp = confusion_matrix(y, ypred).ravel()
print([tn, fp, fn, tp])
fault = len(y[y==1])
normal = len(y) - fault
alpha = fault / len(y)
beta = 1 - alpha
print('得分：%0.3f' %(100*(1-alpha*fp/normal-beta*fn/fault)))