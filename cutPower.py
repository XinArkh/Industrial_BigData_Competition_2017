#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import re
import csv
import numpy as np
import pandas as pd

batch = str(21)  # 15 或 21

data = pd.read_csv('./processed/%s_avg10_data.csv' %batch)
lowPower = data.loc[data['power'] < 2]
lowPower.to_csv('./processed/%s_avg10_lowPower_data.csv' %batch, index=0)