import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns; sns.set()

batch = str(15)
norm = True

data_raw = pd.read_csv('./processed/%s_avg30_lowPower_data.csv' %batch)

# X = np.array(data_raw[['wind_speed', 'power']].values)
# _means = X.mean(axis=0)
# _stds = X.std(axis=0)
# print(_means, _stds)
# stdX = np.zeros(X.shape, dtype=np.float64)
# for i in range(X.shape[1]):
#     stdX[:, i] = (X[:, i] - _means[i]) / _stds[i]
# plt.scatter(stdX[:, 0], stdX[:, 1], c=data_raw['frozen'], s=0.1, cmap='RdBu')

data = data_raw[['wind_speed', 'power']]
if norm:
    data = (data - data.mean()) / (data.std())
plt.scatter(data['wind_speed'], data['power'], c=data_raw['frozen'], s=0.1, cmap='RdBu')

# plt.subplot(1, 2, 1)
# plt.scatter(data['wind_speed'][data_raw['frozen']==0], data['power'][data_raw['frozen']==0], s=0.1, cmap='RdBu')
# lim = plt.axis()
# plt.subplot(1, 2, 2)
# plt.scatter(data['wind_speed'][data_raw['frozen']==1], data['power'][data_raw['frozen']==1], s=0.1, cmap='RdBu')
# plt.axis(lim)

plt.show()