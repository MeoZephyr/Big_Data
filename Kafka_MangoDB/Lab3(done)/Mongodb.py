import json
from pymongo import MongoClient
import chardet
import os
from pathlib import Path
#開啟檔案並檢測編碼方式後回傳
def find_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
    return encoding
def fix_WorkPath():
    #取得當前檔案的目錄路徑，file : 當前檔案路徑 | parent:當前路徑的目錄路徑(上一層路徑)
    path = Path(__file__).parent #尋找目標路徑
    os.chdir(path) #更改工作路徑
    print("path:",path)
    print("fix_WorkPath finished.")
    return path
print("Program started.")
fix_WorkPath() #修正路徑
encoding = find_encoding("config.json")
with open("config.json","r",encoding=encoding) as f:
    config : dict = json.load(f)
client = MongoClient(config["connect_str"])

#db => Mongodb 的特定資料庫
db = client[config["db_name"]]              #連線到指定的資料庫

#確保兩個集合是空的以免重複增加???，db[]
db["RealtimeNearStop"].delete_many({})  #刪除?
db["StopOfRoute"].delete_many({})  


#寫入資料為json檔
encoding = find_encoding("./data/route.json")  
with open("./data/route.json",'r',encoding=encoding) as g:
    sor = json.load(g)
encoding = find_encoding("./data/location.json")  
with open("./data/location.json",'r',encoding=encoding) as g:
    rtns = json.load(g)

data = {}

#for i in :
    #資料處理，先不做

'''
#將每個document 的 _id 設定為i (車牌號碼)後放入集合
for i,j in data.items():
    insert_data = {"_id" : i,"data" : j}
    db["RealtimeNearStop"].insert_one(insert_data)
'''
try:
    db["RealtimeNearStop"].insert_many(rtns)
except:
    print("Insert RealtimeNearStop error:")
try:
    db["StopOfRoute"].insert_many(sor)    #直接插入站牌資料
except:
    print("Insert StopOfRoute error:")

print("Program finished.")