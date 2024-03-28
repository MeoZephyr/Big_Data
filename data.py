# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 17:31:01 2024

@author: C2
"""
from auth import Auth
import requests, json

#票價
url1 = "https://tdx.transportdata.tw/api/basic/v2/Rail/THSR/ODFare?%24format=JSON"
#剩餘座位
url2 = "https://tdx.transportdata.tw/api/basic/v2/Rail/THSR/AvailableSeatStatus/Train/OD/TrainDate/{}/?%24&%24format=JSON"
#時刻表
url3 ="https://tdx.transportdata.tw/api/basic/v2/Rail/THSR/GeneralTimetable?%24top=30&%24format=JSON"
#取得指定[日期]對號座即時剩餘位資料({原始}列車區段Leg角度)
url4="https://tdx.transportdata.tw/api/basic/v2/Rail/THSR/AvailableSeatStatus/Train/Leg/TrainDate/{}?%24&%24format=JSON"
#取得指定[車次]的定期時刻表資料
url5="https://tdx.transportdata.tw/api/basic/v2/Rail/THSR/DailyTimetable/TrainDate/{}?%24format=JSON"
class Data():
    #前置處理取得data_header
    def __init__(self) -> None:
        self.data_header = Auth().get_data_header()        
    def get_data_response(self,url):
        data_response = requests.get(url, headers = self.data_header)
        return json.loads(data_response.text)
    def get_ODFare(self):
        return self.get_data_response(url1)
    def get_AvailableSeat_Status_By_Date(self,date):
        return self.get_data_response(url2.format(date))
    def get_GeneralTime_table(self):
        return self.get_data_response(url3)
    def get_MidwayTrain_test(self,date):
        return self.get_data_response(url4.format(date))
    def get_TrainNO_Inf(self,date):
        return self.get_data_response(url5.format(date))
    def get_OD():
        O = input("請輸入起站:")
        D = input("請輸入迄站:")
        OD = [O,D]
        return  OD
    '''
    #取得目標縣市路線資料
    def get_stop_of_route(self,cname,rname):
        return self.get_data_response(url1.format(cname,rname))

    #取得目標路線名稱
    def get_real_time_near_stop(self,cname,rname):
        return self.get_data_response(url2.format(cname,rname))
    '''




