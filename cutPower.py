#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import re
import csv
import numpy as np
import pandas as pd


def CutPower(batch, minutes):
    data = pd.read_csv('./processed/%s_avg%s_data.csv' %(batch, str(minutes)))
    lowPower = data.loc[data['power'] < 2]
    lowPower.to_csv('./processed/%s_avg%s_lowPower_data.csv' %(batch, str(minutes)), index=0)


if __name__ == '__main__':
    CutPower(batch=str(15), minutes=1)