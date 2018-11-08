import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()


batch = str(15)
minutes = 1
elementList = ['wind_speed', 'power']

data = pd.read_csv('./processed/%s_avg%s_lowPower_data.csv' %(batch, str(minutes)))

X = data[elementList]
X_min = X.min()
X_max = X.max()
X = (X - X_min) / (X_max - X_min)
y = data['frozen']

z = np.polyfit(X['wind_speed'][y==0], X['power'][y==0], 2)
p = np.poly1d(z)

xp = np.linspace(0, 1, 100)
plt.scatter(X['wind_speed'], X['power'], c=y, s=0.1, cmap='RdBu')
plt.plot(xp, p(xp), '-')
plt.axis([0, 1, 0, 1])

C = 1 - X['power'] / p(X['wind_speed'])
# C[X['wind_speed'] <= 0.175] = 0
plt.figure()
plt.scatter(X['wind_speed'], C, c=y, s=0.1, cmap='RdBu')
plt.axis([0, 1, -2, 2])
plt.show()

# C.to_csv('./processed/%s_avg%s_C.csv'
#                  %(batch, str(minutes)), index=0, header='C')

# deltaC = C[]
