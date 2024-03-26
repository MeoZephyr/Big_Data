import requests
import json
from data import Data

class Fare():
    def __init__(self, O, D):
        self.O = O
        self.D = D
        self.data = Data()
        fare_data = self.get_fare()
        fare_info = self.collect_fare(fare_data)
        self.print_fare(fare_info)

    def get_fare(self):
        fare_data = self.data.get_ODFare()
        return fare_data

    def collect_fare(self, data):
        fare_info = []
        TicketType = [('1', '一般票(單程票)'), ('2', '來回票'), ('3', '電子票証(悠遊卡/一卡通)'), ('4', '回數票'), ('5', '定期票(30天期)'),
                      ('6', '定期票(60天期)'), ('7', '早鳥票'), ('8', '團體票')]
        FareClass = [('1', '成人'), ('2', '學生'), ('3', '孩童'), ('4', '敬老'), ('5', '愛心'), ('6', '愛心孩童'), ('7', '愛心優待/愛心陪伴'),
                     ('8', '軍警'), ('9', '法優')]
        CabinClass = [('1', '標準座車廂'), ('2', '商務座車廂'), ('3', '自由座車廂')]

        for journey in data:
            if journey['OriginStationName']['Zh_tw'] == self.O and journey['DestinationStationName']['Zh_tw'] == self.D:
                for fare in journey['Fares']:
                    ticket_type_desc = next((item[1] for item in TicketType if item[0] == str(fare['TicketType'])), '未知票種')
                    fare_class_desc = next((item[1] for item in FareClass if item[0] == str(fare['FareClass'])), '未知身分')
                    cabin_class_desc = next((item[1] for item in CabinClass if item[0] == str(fare['CabinClass'])), '未知車廂')
                    fare_info.append([ticket_type_desc, fare_class_desc, cabin_class_desc, str(fare['Price']) + "元"])
                break
        return fare_info

    def print_fare(self, fare_info):
        for item in fare_info:
            print("票種: {} 身分: {} 車廂: {} 價格: {}".format(item[0], item[1], item[2], item[3]))
            print()
            
#test
#fare_instance = Fare("台北", "南港")
