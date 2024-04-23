import requests
import json

class ChangeseatV2:
    @staticmethod
    def main(arguments):
        app_id = 'B11002064-0b185a9c-e5b5-4196'
        app_key = 'd2da45c3-9a9e-47f2-9b1d-68885bcc08ee'
        auth_url = "https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"
        url = "https://tdx.transportdata.tw/api/basic/v2/Rail/THSR/AvailableSeatStatusList?%24%24format=JSON"
        urlFare = "https://tdx.transportdata.tw/api/basic/v2/Rail/THSR/ODFare?%24format=JSON"

        try:
            d = ChangeseatV2.authenticate(app_id, app_key, auth_url)
            data_response = requests.get(url, headers=d.get_data_header())
            data_Fare = requests.get(urlFare, headers=d.get_data_header())
        except:
            a = ChangeseatV2.Auth(app_id, app_key)
            auth_response = requests.post(auth_url, a.get_auth_header())
            d = ChangeseatV2.data(app_id, app_key, auth_response)
            data_response = requests.get(url, headers=d.get_data_header())   
            data_Fare = requests.get(urlFare, headers=d.get_data_header())   

        station = input("輸入起始車站:")
        endstation = input("輸入終點車站")
        people = input("是否具有愛心敬老孩童其中一種身分(是1否2):")
        num = int(input("人數幾人:"))
        trainSeat = []
        a = json.loads(data_response.text)
        
        keep = {}
        trainID = {}
        for j in a["AvailableSeats"]:
            if j["TrainNo"] == '1514':
                keep = j
                State = j["EndingStationName"]["Zh_tw"]
                for k in j["StopStations"]:
                    trainID[k["StationName"]["Zh_tw"]] = k["StopSequence"]
                    if k["StationName"]["Zh_tw"] == State:
                        num = k["StopSequence"]
                trainID[keep['StationName']['Zh_tw']] = 1

        choise = input("1.標準座 2.商務座 3.自由座")
        choise2 = input("是否接受另一種位置 1 是 2否")
        canseat = ''
        Temp = False
        flag = trainID[endstation]

        # 这里省略了后续的代码，请确保您的 changeseatV2.py 文件的其余部分是有效的

        print(trainSeat)

    class Auth:
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

    class data:
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

    @staticmethod
    def authenticate(app_id, app_key, auth_url):
        a = ChangeseatV2.Auth(app_id, app_key)
        auth_response = requests.post(auth_url, a.get_auth_header())
        return ChangeseatV2.data(app_id, app_key, auth_response)

if __name__ == "__main__":
    ChangeseatV2.main([])
