# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 17:31:01 2024

@author: C2
"""
from auth import Auth
import requests, json

#補路線名稱，url.format() 填補中間缺的兩個參數
#取得指定{縣市}{路線名稱}的市區公車顯示用路線站序資料(取得所有停靠站資料)
url1 = "https://tdx.transportdata.tw/api/basic/v2/Bus/StopOfRoute/City/{}/{}?%24format=JSON"    
#取得指定{縣市}{路線名稱}的公車動態定點資料(A2)(批次更新)(取得當下公車所在地點)
url2 = "https://tdx.transportdata.tw/api/basic/v2/Bus/RealTimeNearStop/City/{}/{}?%24format=JSON"

class Data():
    #前置處理取得data_header
    def __init__(self) -> None:
        self.data_header = Auth().get_data_header()
        
    def get_data_response(self,url):
        data_response = requests.get(url, headers = self.data_header)
        return json.loads(data_response.text)

    #取得目標縣市路線資料
    def get_stop_of_route(self,cname,rname):
        return self.get_data_response(url1.format(cname,rname))

    #取得目標路線名稱
    def get_real_time_near_stop(self,cname,rname):
        return self.get_data_response(url2.format(cname,rname))
    




