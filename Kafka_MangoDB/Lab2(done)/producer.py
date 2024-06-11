# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 18:09:16 2024

@author: C2
"""
from data import Data
import json, time
from kafka import KafkaProducer #似乎只有3.10的直譯器版本可以成功使用
import os
from pathlib import Path
import chardet

def fix_WorkPath():
    #取得當前檔案的目錄路徑，file : 當前檔案路徑 | parent:當前路徑的目錄路徑(上一層路徑)
    path = Path(__file__).parent #尋找目標路徑
    os.chdir(path) #更改工作路徑
    return path
fix_WorkPath() #修正路徑

data = Data()
city = "Taoyuan"
route = "5086"
sor = data.get_stop_of_route(city,route)    #取得目標城市的路線資料
rtns = data.get_real_time_near_stop(city,route)


#先開啟config取得config.json的編碼方式(變數encoding)
with open('config.json', 'rb') as file:
    raw_data = file.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']
print("encoding:",encoding," type:",type(encoding))
with open("config.json","r",encoding=encoding) as f: #讀取config檔案
    config = json.load(f)

#創建producer物件
producer = KafkaProducer(bootstrap_servers = config["server"],  #導入server為config中設定好的server
                         value_serializer=lambda m:json.dumps(m).encode(encoding))  #將json格式或字典轉為字串，以config.json的編碼方式做編碼

#傳入特定班次公車的所有停靠站資訊及當前的動態位置
msg = {"sor":sor,"rtns":rtns}       #將先前取得的資料放入字典
producer.send(config["topic"],msg)  #將訊息(msg) 送出置先前設定好的topic
producer.flush()                    # 確保所有待發送的消息都被發送

time.sleep(5)                       #暫停5秒鐘，讓傳送訊息的動作有緩衝時間
