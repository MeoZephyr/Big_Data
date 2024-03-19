import TDX_Fare
from data import Data

print("輸入欲查詢之起迄站。")
OD = Data.get_OD()

print("取得票價資料:")
TDX_Fare.Fare(OD[0],OD[1]) 

