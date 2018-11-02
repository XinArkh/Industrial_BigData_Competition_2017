#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns; sns.set()


def Plot(batch, minutes, elementList, norm):
    data_raw = pd.read_csv('./processed/%s_avg%s_lowPower_data.csv' %(batch, str(minutes)))
    data = data_raw[elementList]
    if norm:
        data = (data - data.min()) / (data.max() - data.min())
    plt.scatter(data['wind_speed'], data['power'], c=data_raw['frozen'], s=0.1, cmap='RdBu')

    # plt.subplot(1, 2, 1)
    # plt.scatter(data['wind_speed'][data_raw['frozen']==0], data['power'][data_raw['frozen']==0], s=0.1, cmap='RdBu')
    # lim = plt.axis()
    # plt.subplot(1, 2, 2)
    # plt.scatter(data['wind_speed'][data_raw['frozen']==1], data['power'][data_raw['frozen']==1], s=0.1, cmap='RdBu')
    # plt.axis(lim)

    plt.show()


if __name__ == '__main__':
    Plot(batch=str(15), minutes=1, 
        elementList=['wind_speed', 'power'], norm=True)