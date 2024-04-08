import requests
from pprint import pprint #pprint : pretty print，印出的資料會比較整齊
import json
import sys

app_id = 'B11002064-0b185a9c-e5b5-4196'         #輸入TDX會員中心處的app_id
app_key = 'd2da45c3-9a9e-47f2-9b1d-68885bcc08ee'#輸入TDX會員中心處的app_key

auth_url="https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"
url = "https://tdx.transportdata.tw/api/basic/v2/Rail/THSR/AvailableSeatStatusList?%24%24format=JSON"  #透過TDX網址找想要取得的資料，並將此處的url改為網站提供的url(從/v2開始)，資料可用條件篩選

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

if __name__ == '__main__':
    try: #如果auth_response已經存在，則不用再次取得 直接使用
        d = data(app_id, app_key, auth_response) 
        data_response = requests.get(url, headers=d.get_data_header())
    except:#auth_response 不存在，則先取得auth_response，再取得data_response
        a = Auth(app_id, app_key)
        auth_response = requests.post(auth_url, a.get_auth_header())
        d = data(app_id, app_key, auth_response)
        data_response = requests.get(url, headers=d.get_data_header())    


station = input("輸入起始車站:")
endstation=input("輸入終點車站")
trainSeat=[]
a=json.loads(data_response.text)
    # pprint(a)

    #算終點站位置
keep={}
trainID={}
for j in a["AvailableSeats"]:
    if j["TrainNo"]=='1514':
        keep=j
        State=j["EndingStationName"]["Zh_tw"]
        for k in j["StopStations"]:
            trainID[k["StationName"]["Zh_tw"]]=k["StopSequence"]
            if k["StationName"]["Zh_tw"]==State:
                num=k["StopSequence"]
trainID[keep['StationName']['Zh_tw']]=1
    # pprint(trainID)
choise=input("1.標準座 2.商務座")
choise2=input("是否接受另一種位置 1 是 2否")
canseat=''
Temp=False
flag=trainID[endstation]
#---------------------- 乘坐標準座--------------------------------------------
if choise=='1':
#第一次到的位置
    for j in keep["StopStations"]:
        if j["StopSequence"]>flag :
            continue
        if j["StandardSeatStatus"]=='O' or j["StandardSeatStatus"]=='L':
            if j["StopSequence"]>=trainID[station]:
                canseat=j['StationName']['Zh_tw']
                Temp=True
        else:
            break
        # print("可座至",canseat)
    if Temp==True:
        trainSeat.append([station,canseat])
    station=canseat
    Scanseat=canseat
#換位子
    if station!=endstation:
        if choise2=='1':
            while station!=endstation:
                Temp=False
                station=canseat
                a=json.loads(data_response.text)
                keep.clear()
                for j in a["AvailableSeats"]:
                    if(j["TrainNo"]=='1514'):
                        for k in j["StopStations"]:
                            if k["StopSequence"]<=trainID[station] or k["StopSequence"]>trainID[endstation]:
                                continue
                            keep[k["StopSequence"]]=k
                count=trainID[station]+1
                for j in keep:
                    if keep[count]["BusinessSeatStatus"]=='O' or keep[count]["BusinessSeatStatus"]=='L':
                        canseat=keep[count]["StationName"]['Zh_tw']
                        Scanseat=keep[count]["StationName"]['Zh_tw']
                        Temp=True
                    else:
                        break
                    count+=1
                if Temp==True:
                    trainSeat.append([station,canseat])
                else:
                    if trainID[station]+1 in keep:
                        canseat=keep[trainID[station]+1]["StationName"]["Zh_tw"]
                        station=canseat
            Temp=True
            for j in trainSeat:
                if Temp==True:
                    print(j[0],"到",j[1],"有標準座")
                    Temp=False
                else:
                    print(j[0],"到",j[1],"有商務座")
                
        else:
            print("只可坐到",trainSeat[0][1])
    else:
        print("全程皆有位子坐")
#----------------------乘坐商務座------------------------------------------------
if choise=='2':
    for j in keep["StopStations"]:
        if j["StopSequence"]>flag :
            continue
        if j["BusinessSeatStatus"]=='O' or j["BusinessSeatStatus"]=='L':
            if j["StopSequence"]>=trainID[station]:
                canseat=j['StationName']['Zh_tw']
                Temp=True
        else:
            break
        # print("可座至",canseat)
    if Temp==True:
        trainSeat.append([station,canseat])
    station=canseat
    Scanseat=canseat
#換位子
    if station!=endstation:
        if choise2=='1':
            while station!=endstation:
                Temp=False
                station=canseat
                a=json.loads(data_response.text)
                keep.clear()
                for j in a["AvailableSeats"]:
                    if(j["TrainNo"]=='1514'):
                        for k in j["StopStations"]:
                            if k["StopSequence"]<=trainID[station] or k["StopSequence"]>trainID[endstation]:
                                continue
                            keep[k["StopSequence"]]=k
                count=trainID[station]+1
                for j in keep:
                    if keep[count]["StandardSeatStatus"]=='O' or keep[count]["StandardSeatStatus"]=='L':
                        canseat=keep[count]["StationName"]['Zh_tw']
                        Scanseat=keep[count]["StationName"]['Zh_tw']
                        Temp=True
                    else:
                        break
                    count+=1
                if Temp==True:
                    trainSeat.append([station,canseat])
                else:
                    if trainID[station]+1 in keep:
                        canseat=keep[trainID[station]+1]["StationName"]["Zh_tw"]
                        station=canseat
            Temp=True
            for j in trainSeat:
                if Temp==True:
                    print(j[0],"到",j[1],"有商務座")
                    Temp=False
                else:
                    print(j[0],"到",j[1],"有標準座")
        else:
            print("只可坐到",trainSeat[0][1])
    else:
        print("全程皆有位子坐")


                
            

        

                
   

                        






               

