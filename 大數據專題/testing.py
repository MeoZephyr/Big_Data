import TDX_AvailableSeatStatusList_date,TDX_Fare

print("取得票價資料")
data = TDX_Fare.Fare().get_fare() 
print("取得票價資料完成,輸入欲查詢之起迄站")
TDX_Fare.Fare.print_fare(data)
print("取得座位資料")
TDX_AvailableSeatStatusList_date.Seat()
