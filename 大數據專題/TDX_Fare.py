import requests
import json
from data import Data

class Fare():
    '''
    #下方兩個函式取代本來的code，最終取得data_response(json格式)
    def __init__(self) -> None:
        self.data_header = Auth().get_data_header()
    def get_data_response(self,url):
        data_response = requests.get(url, headers = self.data_header)
        return json.loads(data_response.text)
    '''
    
    #self mean what??
    def get_fare(self):
        get_data = Data().get_ODFare()
        TicketType = {"1":'一般票(單程票)',"2":'來回票',"3":'電子票証(悠遊卡/一卡通)',"4":'回數票',"5":'定期票(30天期)',"6":'定期票(60天期)',"7":'早鳥票',"8":'團體票'}
        FareClass = {"1":'成人',"2":'學生',"3":'孩童',"4":'敬老',"5":'愛心',"6":'愛心孩童',"7":'愛心優待/愛心陪伴',"8":'軍警',"9":'法優'}
        CabinClass = {"1":'標準座車廂',"2":'商務座車廂',"3":'自由座車廂'}

        all = dict()
        for i in get_data:
            TFC_list = []
            price_list = []
            fare = i['Fares']
            name = i['OriginStationName']['Zh_tw']+'_'+i['DestinationStationName']['Zh_tw']
            for j in fare:
                #print(j)   
                TFC_str = str(j['TicketType'])+str(j['FareClass'])+str(j['CabinClass'])
                TFC_list.append(TFC_str)
                price_list.append(j['Price'])
            all[name] = dict(zip(TFC_list,price_list))

        re_data = dict()
        OD = []
        TFCP = []
        temp = 0
        for i in all:
            OD.append(i[0:2]+"_"+i[3:5])
            buff = []
            for j in all[i]:
                buf = []
                buf.append(TicketType[j[0]])
                buf.append(FareClass[j[1]])
                buf.append(CabinClass[j[2]])
                buf.append(str(all[i][j]))
                buff.append(buf)
            TFCP.append(buff)
        re_data = dict(zip(OD,TFCP))
        return re_data
    
    def print_fare(data):
        start = input("請輸入起站:")
        end   = input("請輸入迄站:")
        key = start+"_"+end
        for i in data[key]:
            print("票種:"+i[0]+" 身分:"+i[1]+" 車廂:"+i[2]+" 價格:"+i[3]+"元")
            print()
        #print("OD:",OD,end="\n\n")
        #print("TFCP:",TFCP,end="\n\n")
        #print("re_data:",re_data,end="\n\n")

if __name__ == '__main__':
    dd = Fare().get_fare()
    Fare.print_fare(dd)

