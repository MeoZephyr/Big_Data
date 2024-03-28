# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 20:25:29 2024

@author: 郭嘉勛
"""

import json
from data import Data
from datetime import datetime
import TDX_AvailableSeatStatusList_date as midway



def __init__(O,D) :
    date = input("輸入日期(格式:yyyy-mm-dd)MidWay:")
    direction_list=["左營","台南","嘉義","雲林","彰化","台中","苗栗","新竹","桃園","板橋","台北","南港"]
    
    if direction_list.index(O) < direction_list.index(D):
        print("北上")
        direction = 1
    else:
        print("南下")
        direction = 0
        
    mid_data = Data().get_MidwayTrain_test(date)
    mm = Data().get_MidwayTrain_test(date)
    data=json.loads(json.dumps(mm))
    if data:
      with open('Data_Seat_Status.json', 'w') as f:
        json.dump(data, f, indent=4,ensure_ascii=False)
    else:
      print('Failed to download data')
#------------------------------------------------------------------    
    mm = Data().get_AvailableSeat_Status_By_Date(date)
    data=json.loads(json.dumps(mm))
    if data:
      with open('Data_Seat_Check.json', 'w') as f:
        json.dump(data, f, indent=4,ensure_ascii=False)
    else:
      print('Failed to download data')
#------------------------------------------------------------------      
    data = json.loads(json.dumps(Data().get_TrainNO_Inf(date)))
    if data:
        with open('data_train_inf.json','w') as f:
            json.dump(data,f,indent=4,ensure_ascii=False)
            
    ShowMidWay(O,D,mid_data,date,direction)
    
    
def ShowMidWay(StartStation,EndStation,mid_data,date,direction):
    seat = {'O':'尚有座位','L':'座位有限','X':'已無座位'} 
    temp = StartStation
    TrainNo=[]
    midway.check(StartStation, EndStation, date ,TrainNo)
    for j in TrainNo:
        for i in mid_data["AvailableSeats"]:
            if i["TrainNo"] == j:
                print("班次:",i["TrainNo"],end = " ")
                with open('data_train_inf.json','r') as f:
                    seat_inf = json.load(f)
                    for a in range(len(seat_inf)):
                        if seat_inf[a]["DailyTrainInfo"]["TrainNo"] == i["TrainNo"]:
                            for q in seat_inf[a]["StopTimes"]:
                                if q["StationName"]["Zh_tw"] == StartStation:
                                    print(q["StationName"]["Zh_tw"],"到",end = " ")
                                    O_time = q["ArrivalTime"]
                                if q["StationName"]["Zh_tw"] == EndStation:
                                    print(q["StationName"]["Zh_tw"])
                                    D_time = q["ArrivalTime"]
                    print("時間:",O_time,"-",D_time)
                 
                #print("端點站:",i["StartingStationName"]["Zh_tw"]," 到 ",i["EndingStationName"]["Zh_tw"])  
                for j in i["StopStations"]:
                    if j["StationName"]["Zh_tw"] == temp :
                        Train_Find = []
                        if seat[j["StandardSeatStatus"]] == "尚有座位" or seat[j["StandardSeatStatus"]] == "座位有限":
                            if j["StationName"]["Zh_tw"] == EndStation or j["NextStationName"]["Zh_tw"] == EndStation:
                                print(i["TrainNo"],"次全程皆有座\n")
                                print("---------------------------")
                                break
                            temp = j["NextStationName"]["Zh_tw"]
                        else:
                            print(i["TrainNo"],"次只能到達",temp,"站",end=",")
                            find_train(temp,EndStation,date,i["TrainNo"],direction)
                            print("\n---------------------------")
                            break
                                  
def find_train(StartStation,EndStation,date,TrainNo_Find,direction):
    with open('data_train_inf.json','r') as f:
        Train = json.load(f)
        count=0
        for i in range(len(Train)):
            if Train[i]["DailyTrainInfo"]["Direction"] == direction:
                if Train[i]["DailyTrainInfo"]["TrainNo"] == TrainNo_Find:
                    print("抵達時間:",end="")
                    for j in Train[i]["StopTimes"]:
                        if j["StationName"]["Zh_tw"] == StartStation:
                            print(j["ArrivalTime"])
                            start_time = datetime.strptime(j["ArrivalTime"], "%H:%M")
                            i+=1
                            break
    
                    for z in range(len(Train)):
                        if Train[z]["DailyTrainInfo"]["Direction"] == direction:
                            for x in Train[z]["StopTimes"]:
    
                                if x["StationName"]["Zh_tw"] == StartStation and count <= 0:
                                    end_time = datetime.strptime(x["ArrivalTime"], "%H:%M")
                                    
                                    if midway.check_seat(StartStation, EndStation, date, Train[z]["DailyTrainInfo"]["TrainNo"]) == "還有座位":                   
                                        if end_time > start_time:
                                            
                                            print("下一班次:",Train[z]["DailyTrainInfo"]["TrainNo"],"次",end="")
                                            print("出發時間:",x["DepartureTime"])
                                            # 計算時間差
                                            time_delta = end_time - start_time
                                            
                                            # 提取時間差中的秒數
                                            seconds = time_delta.seconds
                                            
                                            # 將秒數轉換為小時、分鐘和秒數
                                            hours = seconds // 3600
                                            minutes = (seconds % 3600) // 60

                                            # 輸出結果
                                            print("需在",StartStation,"等待",f"{hours} 小時 {minutes} 分鐘 ",end="")
                                            print(" 轉乘",Train[z]["DailyTrainInfo"]["TrainNo"],"次(出發時間:",x["DepartureTime"],")列車到",EndStation)
                                            count+=1
                                    else :
                                        z+=1
