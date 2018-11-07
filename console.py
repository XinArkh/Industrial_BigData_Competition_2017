#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from labelGen import LabelGen
from avgData import AvgData
from cutPower import CutPower
from plot import Plot
from svm_method import SVM_Method
from score import Score

batch = str(15)
minutes = 1
elementList = ['wind_speed', 'pitch1_angle', 'pitch1_speed', 'power']
norm=True

# LabelGen(batch=batch)

# AvgData(batch=batch, minutes=minutes)

# CutPower(batch=batch, minutes=minutes)

SVM_Method(batch=batch, minutes=minutes, 
    elementList=elementList, norm=norm)

Score(batch=batch, minutes=minutes, 
    elementList=elementList, norm=norm)

Plot(batch=batch, minutes=minutes, 
    elementList=['wind_speed', 'power'], norm=norm)