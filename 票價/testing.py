import TDX_AvailableSeatStatusList_date,TDX_Fare,TDX_GeneralTimetable
from data import Data

print("輸入欲查詢之起迄站。")
OD = Data.get_OD()

print("取得票價資料:")
TDX_Fare.Fare(OD[0],OD[1]) 

print("取得座位資料")
TDX_AvailableSeatStatusList_date.Seat(OD[0],OD[1])

print("取得時刻表")
TDX_GeneralTimetable.GTT().print_table()
