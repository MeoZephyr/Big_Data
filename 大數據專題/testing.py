import TDX_AvailableSeatStatusList_date #傳入起訖站&建構元輸入日期 取得座位資料
import TDX_Fare #傳入起訖站 取得票價資料
import TDX_GeneralTimetable             #取得時刻表
from data import Data
import os
import sys
from pathlib import Path
#pathlib.Path(__file__).parent.absolute()
#print(pathlib.Path().absolute()) #當前工作目錄路徑

work_path = os.getcwd() #當前工作目錄路徑
print("work_path:",work_path)
#取得當前檔案的目錄路徑，__file__ : 當前檔案路徑 | parent:當前路徑的目錄路徑
#path = Path(__file__).parent #尋找目標路徑
#os.chdir(path) #更改工作路徑

# def print_fare(data,start,end):  
#         result = ""
#         key = start+"_"+end
#         for i in data[key]:
#             result += "票種:"+i[0]+" 身分:"+i[1]+" 車廂:"+i[2]+" 價格:"+i[3]+"元"
#             result += "\n"
#             # list.append("票種:"+i[0]+" 身分:"+i[1]+" 車廂:"+i[2]+" 價格:"+i[3]+"元")
#             # list.append("\n")
#         return result
def print_aa():
    print("aa")
    return "aa"
print("輸入欲查詢之起迄站。")
#OD = Data.get_OD() 
# 輸入:台北 左營 2024-05-10
OD = sys.argv[1:3]
date = sys.argv[3]
print("OD:",OD, "type:",type(OD))
print("date:",date, "type:",type(date))
print("-----------------------------")
print("取得票價資料:")
# dd = TDX_Fare.Fare(OD[0],OD[1])
dd = TDX_Fare.get_fare()
# print("call get_fare() success")
result = TDX_Fare.print_fare(dd,OD[0],OD[1])
print(result)
# b = print_aa()
# print(b)
# with open("fare.txt","w") as f:
# f.write(result)
print("取得座位資料")
TDX_AvailableSeatStatusList_date.Seat(OD[0],OD[1],date)

print("取得時刻表")
TDX_GeneralTimetable.GTT().print_table()

