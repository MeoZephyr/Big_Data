
import os
import json
import datetime
import time
try:
    import requests
    print("requests module found")
except ImportError:
    print("requests module not found. Installing...")
    os.system('pip install requests')
    time.sleep( 5 )
    import requests
try:
    from pprint import pprint
    print("pprint module found")
except ImportError:
    print("pprint module not found. Installing...")
    os.system('pip install pprint')
    time.sleep( 5 )
    from pprint import pprint
try:
    from pathlib import Path
    print("pathlib module found")
except ImportError:
    print("pathlib module not found. Installing...")
    os.system('pip install pathlib')
    time.sleep( 5 )
    from pathlib import Path
#取得當前檔案的目錄路徑，__file__ : 當前檔案路徑 | parent:當前路徑的目錄路徑
path = Path(__file__).parent #目標路徑
os.chdir(path) #更改工作路徑
print(path)
print("path set done!")
# from pathlib import Path
# import requests
# from pprint import pprint
class Auth():

    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key

    def get_auth_header(self):
        content_type = 'application/x-www-form-urlencoded'
        grant_type = 'client_credentials'

        return{
            'content-type' : content_type,
            'grant_type' : grant_type,
            'client_id' : self.app_id,
            'client_secret' : self.app_key
        }

class data():

    def __init__(self, app_id, app_key, auth_response):
        self.app_id = app_id
        self.app_key = app_key
        self.auth_response = auth_response

    def get_data_header(self):
        auth_JSON = json.loads(self.auth_response.text)
        access_token = auth_JSON.get('access_token')

        return{
            'authorization': 'Bearer '+access_token
        }

# def get_data_response(url,urlname):
#     try: #如果auth_response已經存在，則不用再次取得 直接使用
#         d = data(app_id, app_key, auth_response) 
#         data_response = requests.get(url, headers=d.get_data_header())
#     except:#auth_response 不存在，則先取得auth_response，再取得data_response
#         a = Auth(app_id, app_key)
#         auth_response = requests.post(auth_url, a.get_auth_header())
#         d = data(app_id, app_key, auth_response)
#         data_response = requests.get(url, headers=d.get_data_header())    
#         Datetime = datetime.datetime.now()
#         Datetime = Datetime.strftime("%Y%m%d_%H_%M_%S")
#         filename = urlname+"_"+Datetime+".json"        
#         with open(filename, 'w') as f:
#             json.dump(data_response.json(), f)
def get_data_response(url, urlname,Datetime):
    try:
        try:
            # 嘗試使用先前獲取的 auth_response
            d = data(app_id, app_key, auth_response) 
            data_response = requests.get(url, headers=d.get_data_header())
            print("auth_response found!")
        except NameError:
            # 如果 auth_response 未定義，則先獲取它
            print("auth_response not found!")
            a = Auth(app_id, app_key)
            auth_response = requests.post(auth_url, a.get_auth_header())
            print("auth_response get done!")
            d = data(app_id, app_key, auth_response)
            data_response = requests.get(url, headers=d.get_data_header())
        
        # 檢查回應的狀態碼
        try:
            data_response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print("data_response.raise_for_status() error")
            print(f"Error fetching data from {urlname}: {e}")
        # 如果一切順利，寫入 JSON 文件
        count = Datetime.strftime("%Y%m%d_%H_%M_%S")
        filename = f"{urlname}_{count}.json"        
        try:
            with open(filename, 'w') as f:
                json.dump(data_response.json(), f)
        except Exception as e:
            print(f"Error writing data to {filename}: {e}")
        date = Datetime.strftime("%Y-%m-%d")
        print(f"{urlname} Date:{date}done!")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {urlname}: {e}")

if __name__ == '__main__':

    app_id = 'b11002048-6daacd6d-abea-4e80'         #輸入TDX會員中心處的app_id
    app_key = '7435f26a-c735-4069-9622-08367c809cd7'#輸入TDX會員中心處的app_key

    auth_url="https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"
    #票價
    url1 = "https://tdx.transportdata.tw/api/basic/v2/Rail/THSR/ODFare?%24format=JSON"
    #剩餘座位
    url2 = "https://tdx.transportdata.tw/api/basic/v2/Rail/THSR/AvailableSeatStatus/Train/OD/TrainDate/{}/?%24&%24format=JSON"
    #時刻表
    url3 ="https://tdx.transportdata.tw/api/basic/v2/Rail/THSR/GeneralTimetable?%24format=JSON"
    #取得指定[日期]對號座即時剩餘位資料({原始}列車區段Leg角度)
    url4="https://tdx.transportdata.tw/api/basic/v2/Rail/THSR/AvailableSeatStatus/Train/Leg/TrainDate/{}?%24&%24format=JSON"
    #取得指定[車次]的定期時刻表資料
    url5="https://tdx.transportdata.tw/api/basic/v2/Rail/THSR/DailyTimetable/TrainDate/{}?%24format=JSON"
    #取得動態對號座剩餘座位資訊看板資料
    url6 = "https://tdx.transportdata.tw/api/basic/v2/Rail/THSR/AvailableSeatStatusList?%24%24format=JSON"  

    print("url set done!")
    Datetime = datetime.datetime.now()
    date = Datetime.strftime("%Y-%m-%d")
    print("Datetime get done! =>",date)


    day = int(input("輸入數字n，代表抓第n天的資料(今天為第0天):"))
    
    newDay = Datetime+datetime.timedelta(days=day)
    i = 0
    # while i<=int(days):
    get_data_response(url1,"ODFare",newDay)
    get_data_response(url2.format(newDay.strftime("%Y-%m-%d")),"AvailableSeatStatus(OD)",newDay)
    get_data_response(url3,"GeneralTimetable",newDay)
    get_data_response(url4.format(newDay.strftime("%Y-%m-%d")),"AvailableSeatStatus(Leg)",newDay)
    get_data_response(url5.format(newDay.strftime("%Y-%m-%d")),"DailyTimetable",newDay)
    get_data_response(url6,"AvailableSeatStatusList",newDay)
        # newDay = newDay+datetime.timedelta(days=1)#放在結尾
        # i+=1
    
    #不須指定日期:get_data_response(url,urlname,Datetime)  type:url,str,datetime(str)
    #需指定日期:get_data_response(url.format(Datetime.strftime("%Y-%m-%d")),urlname,Datetime)  type:url,str,datetime(str)
    # get_data_response(url1,"ODFare",Datetime)
    # get_data_response(url2.format(Datetime.strftime("%Y-%m-%d")),"AvailableSeatStatus(OD)",Datetime)
    # get_data_response(url3,"GeneralTimetable",Datetime)
    # get_data_response(url4.format(Datetime.strftime("%Y-%m-%d")),"AvailableSeatStatus(Leg)",Datetime)
    # get_data_response(url5.format(Datetime.strftime("%Y-%m-%d")),"DailyTimetable",Datetime)
    # get_data_response(url6,"AvailableSeatStatusList",Datetime) 





