# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 14:22:05 2024

@author: 郭嘉勛
"""

import MidWayTrain
from data import Data

print("輸入欲查詢之起迄站。")
OD = Data.get_OD()

print("中途站測試")
MidWayTrain.__init__(OD[0], OD[1])





















