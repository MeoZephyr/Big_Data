import requests
import json
import chardet

auth_url="https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"

class Auth():

    def __init__(self) -> None:
        with open('config.json', 'rb') as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
        with open("./config.json","r",encoding=encoding) as f:  #開檔
            acc = json.load(f)
            self.app_id = acc["app_id"]   #從config 取得id 及secret
            self.app_key = acc["app_key"]

    def get_auth_header(self):
        content_type = 'application/x-www-form-urlencoded'
        grant_type = 'client_credentials'

        #URL 所需要的header
        return{ 
            'content-type' : content_type,
            'grant_type' : grant_type,
            'client_id' : self.app_id,
            'client_secret' : self.app_key
        }
    
    def get_data_header(self):
        self.auth_response = requests.post(auth_url, self.get_auth_header())
        auth_JSON = json.loads(self.auth_response.text) #取得token
        access_token = auth_JSON.get('access_token')

        return{
            'authorization': 'Bearer ' + access_token,
            'Accept-Encoding': 'gzip'
        }



