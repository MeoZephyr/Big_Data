import requests
import json

auth_url="https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"


class Auth():
    def __init__(self) -> None:
        print("Auth init begin!")
        with open("./config.json","r") as f:  #開檔
            acc = json.load(f)
            self.app_id = acc["app_id"]   #從config 取得id 及secret
            self.app_key = acc["app_key"]
        print("Auth init done!")

    def get_auth_header(self):
        print("getting auth header.")
        content_type = 'application/x-www-form-urlencoded'
        grant_type = 'client_credentials'

        print("auth done then return")
        #URL 所需要的header
        return{ 
            'content-type' : content_type,
            'grant_type' : grant_type,
            'client_id' : self.app_id,
            'client_secret' : self.app_key
        }
    
    def get_data_header(self):
        print("getting data header.")
        self.auth_response = requests.post(auth_url, self.get_auth_header())
        auth_JSON = json.loads(self.auth_response.text) #取得token
        access_token = auth_JSON.get('access_token')
        print("done then return")
        return{
            'authorization': 'Bearer ' + access_token,
            'Accept-Encoding': 'gzip'
        }



