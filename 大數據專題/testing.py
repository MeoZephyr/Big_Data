import TDX_AvailableSeatStatusList_date,TDX_Fare,TDX_GeneralTimetable
from data import Data
import os
from pathlib import Path

#pathlib.Path(__file__).parent.absolute()
#print(pathlib.Path().absolute()) #當前工作目錄路徑

work_path = os.getcwd() #當前工作目錄路徑
print(work_path)
#取得當前檔案的目錄路徑，__file__ : 當前檔案路徑 | parent:當前路徑的目錄路徑
#path = Path(__file__).parent #目標路徑
#os.chdir(path) #更改工作路徑

'''
print("輸入欲查詢之起迄站。")
OD = Data.get_OD()

print("取得票價資料:")
TDX_Fare.Fare(OD[0],OD[1]) 
'''
'''
print("取得座位資料")
TDX_AvailableSeatStatusList_date.Seat(OD[0],OD[1])

print("取得時刻表")
TDX_GeneralTimetable.GTT().print_table()
'''

