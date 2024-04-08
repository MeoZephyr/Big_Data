import requests
from pprint import pprint #pprint : pretty print，印出的資料會比較整齊
import json

app_id = 'b11002048-6daacd6d-abea-4e80'         #輸入TDX會員中心處的app_id
app_key = '7435f26a-c735-4069-9622-08367c809cd7'#輸入TDX會員中心處的app_key

auth_url="https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"
url = "https://tdx.transportdata.tw/api/basic/v2/Rail/THSR/ODFare?%24format=JSON"  #透過TDX網址找想要取得的資料，並將此處的url改為網站提供的url(從/v2開始)，資料可用條件篩選
#EX: url = "https://tdx.transportdata.tw/api/basic/v2/Rail/THSR/AvailableSeatStatusList?$top=3&$format=JSON"  
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


#price=[[[0]*8 for i in range(9)] for i in range(3)]# price[3][9][8]: 3種車廂，9種身分，8種票卷[CabinClass][FareClass][TicketType]
data = json.loads(data_response.text) #json.loads() : 將json格式轉為python物件
TicketType = {"1":'一般票(單程票)',"2":'來回票',"3":'電子票証(悠遊卡/一卡通)',"4":'回數票',"5":'定期票(30天期)',"6":'定期票(60天期)',"7":'早鳥票',"8":'團體票'}
FareClass = {"1":'成人',"2":'學生',"3":'孩童',"4":'敬老',"5":'愛心',"6":'愛心孩童',"7":'愛心優待/愛心陪伴',"8":'軍警',"9":'法優'}
CabinClass = {"1":'標準座車廂',"2":'商務座車廂',"3":'自由座車廂'}

all = dict()
for i in data:
    TFC_list = []
    price_list = []
    fare = i['Fares']
    name = i['OriginStationName']['Zh_tw']+'_'+i['DestinationStationName']['Zh_tw']
    for j in fare:
        #print(j)   
        TFC = str(j['TicketType'])+str(j['FareClass'])+str(j['CabinClass'])
        TFC_list.append(TFC)
        price_list.append(j['Price'])
    all[name] = dict(zip(TFC_list,price_list))
    #三組對照印出測試
    '''print("fare",fare)
    print()
    print(TFC_list)
    print(price_list)
    print()
    print(all)
    break
    '''
start=input("起點車站:")
end=input("終點車站:")
name=start+"_"+end
people=input("是否具有愛心敬老孩童其中一種身分(是1否2):")
num=int(input("人數幾人:"))
seat=input("要搭自由座還是標準座還是商務座(1標準 2商務 3自由)")
ticket=[]
if seat=='1':
    ticket.append("111")
    if num>=11:
        ticket.append("811")
    if people=='1':
        ticket.append("191")
if seat=='2':
    ticket.append("112")
    if num>=11:
        ticket.append("812")
    if people=='1':
        ticket.append("192")
if seat=='3':
    ticket.append("113")
    if people=='1':
        ticket.append("193")
price=10000
endticket=""
for i in ticket:
    if i in all[name]:
        if all[name][i]<price:
            endticket=i
            price=all[name][i]
print("選擇",TicketType[endticket[0]],FareClass[endticket[1]],"票種 = ",price,"元會是最省錢的方法")
# for i in all:
#     print("起站:"+i[0:2]+" 迄站:"+i[3:5])
#     for j in all[i]:
#         print("票種:"+TicketType[j[0]]+" 身分:"+FareClass[j[1]]+" 車廂:"+CabinClass[j[2]]+" 價格:"+str(all[i][j])+"元")
#     print()
