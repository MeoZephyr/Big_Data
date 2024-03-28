# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 20:25:29 2024

@author: 郭嘉勛
"""

import requests,json
from data import Data
import TDX_AvailableSeatStatusList_date as midway
def __init__(O,D) :
    date = input("輸入日期(格式:yyyy-mm-dd)MidWay:")
    mid_data = Data().get_MidwayTrain_test(date)
    ShowMidWay(O,D,mid_data,date)
    
    
def ShowMidWay(StartStation,EndStation,mid_data,date):
    seat = {'O':'尚有座位','L':'座位有限','X':'已無座位'} 
    temp = StartStation
    TrainNo=[]
    midway.check(StartStation, EndStation, date ,TrainNo)
    for j in TrainNo:
        for i in mid_data["AvailableSeats"]:
            if i["TrainNo"] == j:
                print("班次:",i["TrainNo"])
                print("端點站:",i["StartingStationName"]["Zh_tw"]," 到 ",i["EndingStationName"]["Zh_tw"])
                
                for j in i["StopStations"]:
                    
                    
                   if j["StationName"]["Zh_tw"] == temp:
                       if seat[j["StandardSeatStatus"]] == "尚有座位" or seat[j["StandardSeatStatus"]] == "座位有限":
                           if j["StationName"]["Zh_tw"] == EndStation:
                               print(i["TrainNo"],"次全程皆有座\n")
                               print("---------------------------")
                               break
                           temp = j["NextStationName"]["Zh_tw"]
                       else:
                           print(i["TrainNo"],"次只能到達",temp,"站  需在",temp,"換班次")
                           print("---------------------------")
                           break
                       
                       """print(j["StationName"]["Zh_tw"],"-->",j["NextStationName"]["Zh_tw"])
                       print("標準座:",seat[j["StandardSeatStatus"]])
                       print("商務座:",seat[j["BusinessSeatStatus"]])
                       print()
                       print("-----------------------\n")"""
            
            
                
