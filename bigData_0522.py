import requests
import json
import tkinter as tk

app_id = 'B11002064-0b185a9c-e5b5-4196'
app_key = 'd2da45c3-9a9e-47f2-9b1d-68885bcc08ee'

auth_url = "https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"
url = "https://tdx.transportdata.tw/api/basic/v2/Rail/THSR/AvailableSeatStatusList?%24%24format=JSON"
urlFare = "https://tdx.transportdata.tw/api/basic/v2/Rail/THSR/ODFare?%24format=JSON"

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

class Data():
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

def calculate_fare(station, endstation, people, num, choise, choise2):
    start_station = station.get()
    end_station = endstation.get()
    people_status = people.get()
    num_passengers = int(num.get())
    seat_choice = choise.get()
    accept_other_seat = choise2.get()
    alltrain = set()

    try:
        d = Data(app_id, app_key, auth_response)
        data_response = requests.get(url, headers=d.get_data_header())
        data_Fare = requests.get(urlFare, headers=d.get_data_header())
    except:
        a = Auth(app_id, app_key)
        auth_response = requests.post(auth_url, a.get_auth_header())
        d = Data(app_id, app_key, auth_response)
        data_response = requests.get(url, headers=d.get_data_header())
        data_Fare = requests.get(urlFare, headers=d.get_data_header())

    trainSeat = []
    a = json.loads(data_response.text)
    keep = {}
    trainID = {}

    for j in a["AvailableSeats"]:
        flag1 = 0
        flag2 = 0
        for k in j["StopStations"]:
            if k["StationName"]["Zh_tw"] == realstation:
                flag1 = 1
            if k["StationName"]["Zh_tw"] == endstation and flag1 == 1:
                flag2 = 1
        if flag1 == 1 and flag2 == 1:
            alltrain.add(j["TrainNo"])
    for x in alltrain:
        station = realstation
        trainSeat = []
        a = json.loads(data_response.text)
        keep = {}
        trainID = {}
        for j in a["AvailableSeats"]:
            if j["TrainNo"] == x:
                keep = j
                State = j["EndingStationName"]["Zh_tw"]
                for k in j["StopStations"]:
                    trainID[k["StationName"]["Zh_tw"]] = k["StopSequence"]
                    if k["StationName"]["Zh_tw"] == State:
                        num = k["StopSequence"]
                trainID[keep['StationName']['Zh_tw']] = 1

        canseat = ''
        Temp = False
        flag = trainID[endstation]

        if seat_choice == '1':
            for j in keep["StopStations"]:
                if j["StationName"]["Zh_tw"] == start_station:
                    continue
                if j["StopSequence"] > flag:
                    continue
                if j["StandardSeatStatus"] == 'O' or j["StandardSeatStatus"] == 'L':
                    if j["StopSequence"] >= trainID[start_station]:
                        canseat = j['StationName']['Zh_tw']
                        Temp = True
                else:
                    break

            if Temp:
                trainSeat.append([start_station, canseat, '1'])
            station = canseat
            Scanseat = canseat

            if station != end_station:
                if accept_other_seat == '1':
                    while station != end_station:
                        Temp = False
                        station = canseat
                        a = json.loads(data_response.text)
                        keep.clear()
                        for j in a["AvailableSeats"]:
                            if j["TrainNo"] == '1514':  # 1514 --> x
                                for k in j["StopStations"]:
                                    if k["StopSequence"] <= trainID[station] or k["StopSequence"] > trainID[end_station]:
                                        continue
                                    keep[k["StopSequence"]] = k
                        count = trainID[station] + 1
                        for j in keep:
                            if keep[count]["BusinessSeatStatus"] == 'O' or keep[count]["BusinessSeatStatus"] == 'L':
                                canseat = keep[count]["StationName"]['Zh_tw']
                                Scanseat = keep[count]["StationName"]['Zh_tw']
                                Temp = True
                            else:
                                break
                            count += 1
                        if Temp:
                            trainSeat.append([station, canseat, '2'])
                        else:
                            if trainID[station] + 1 in keep:
                                canseat = keep[trainID[station] + 1]["StationName"]["Zh_tw"]
                                station = canseat

        elif seat_choice == '2':
            for j in keep["StopStations"]:
                if j["StopSequence"] > trainID[end_station]:
                    continue
                if j["BusinessSeatStatus"] == 'O' or j["BusinessSeatStatus"] == 'L':
                    if j["StopSequence"] >= trainID[start_station]:
                        canseat = j['StationName']['Zh_tw']
                        Temp = True
                else:
                    break

            if Temp:
                trainSeat.append([start_station, canseat, '2'])
            station = canseat
            Scanseat = canseat

            if station != end_station:
                if accept_other_seat == '1':
                    while station != end_station:
                        Temp = False
                        station = canseat
                        a = json.loads(data_response.text)
                        keep.clear()
                        for j in a["AvailableSeats"]:
                            if j["TrainNo"] == '1514':
                                for k in j["StopStations"]:
                                    if k["StopSequence"] <= trainID[station] or k["StopSequence"] > trainID[end_station]:
                                        continue
                                    keep[k["StopSequence"]] = k
                        count = trainID[station] + 1
                        for j in keep:
                            if keep[count]["StandardSeatStatus"] == 'O' or keep[count]["StandardSeatStatus"] == 'L':
                                canseat = keep[count]["StationName"]['Zh_tw']
                                Scanseat = keep[count]["StationName"]['Zh_tw']
                                Temp = True
                            else:
                                break
                            count += 1
                        if Temp:
                            trainSeat.append([station, canseat, '1'])
                        else:
                            if trainID[station] + 1 in keep:
                                canseat = keep[trainID[station] + 1]["StationName"]["Zh_tw"]
                                station = canseat
                    Temp = True

    data = json.loads(data_Fare.text)
    TicketType = {"1": '一般票(單程票)', "2": '來回票', "3": '電子票証(悠遊卡/一卡通)', "4": '回數票', "5": '定期票(30天期)',
                  "6": '定期票(60天期)', "7": '早鳥票', "8": '團體票'}
    FareClass = {"1": '成人', "2": '學生', "3": '孩童', "4": '敬老', "5": '愛心', "6": '愛心孩童', "7": '愛心優待/愛心陪伴',
                 "8": '軍警', "9": '法優'}
    CabinClass = {"1": '標準座車廂', "2": '商務座車廂', "3": '自由座車廂'}

    all_fares = dict()
    for i in data:
        TFC_list = []
        price_list = []
        fare = i['Fares']
        name = i['OriginStationName']['Zh_tw'] + '_' + i['DestinationStationName']['Zh_tw']
        for j in fare:
            TFC = str(j['TicketType']) + str(j['FareClass']) + str(j['CabinClass'])
            TFC_list.append(TFC)
            price_list.append(j['Price'])
        all_fares[name] = dict(zip(TFC_list, price_list))

    for i in trainSeat:
        start = i[0]
        end = i[1]
        name = start + "_" + end
        ticket = []
        if i[2] == '1':
            ticket.append("111")
            if num_passengers >= 11:
                ticket.append("811")
            if people_status == '1':
                ticket.append("191")
        if i[2] == '2':
            ticket.append("112")
            if num_passengers >= 11:
                ticket.append("812")
            if people_status == '1':
                ticket.append("192")
        price = 10000
        endticket = ""
        for j in ticket:
            if j in all_fares[name]:
                if all_fares[name][j] < price:
                    endticket = j
                    price = all_fares[name][j]
        if i[2] == '1':
            result_text.insert("end", "坐標準座從" + start + "坐到" + end + "要" + str(price) + "元\n")
            # print("坐標準座從", start, "坐到", end, "要", price, 坐商務坐從" + start + "坐到" + end + "要" + str(price) + "元\n")
            # print("坐商務坐從", start, "坐到","元")
        if i[2] == '2':
            result_text.insert("end", end, "要", price , "元")

    if seat_choice == '3':
        name = start_station + "_" + end_station
        ticket = []
        ticket.append("113")
        if people_status == '1':
            ticket.append("193")
        price = 10000
        endticket = ""
        for j in ticket:
            if j in all_fares[name]:
                if all_fares[name][j] < price:
                    endticket = j
                    price = all_fares[name][j]
        result_text.insert("end", "坐自由座從 " + start_station + " 到 " + end_station + " 要 " + str(price) + " 元\n")
        # ("坐自由座從", start_station, "到", end_station, "要", price, "元")


root = tk.Tk()
root.title("高鐵車票")

start_station_label = tk.Label(root, text="起始車站：")
start_station_label.grid(row=0, column=0, padx=5, pady=5)
station = tk.Entry(root)
station.grid(row=0, column=1, padx=5, pady=5)

end_station_label = tk.Label(root, text="終點車站：")
end_station_label.grid(row=1, column=0, padx=5, pady=5)
endstation = tk.Entry(root)
endstation.grid(row=1, column=1, padx=5, pady=5)

people_label = tk.Label(root, text="是否具有愛心敬老孩童其中一種身分(是1否2)：")
people_label.grid(row=2, column=0, padx=5, pady=5)
people = tk.Entry(root)
people.grid(row=2, column=1, padx=5, pady=5)

num_passengers_label = tk.Label(root, text="乘客人數：")
num_passengers_label.grid(row=3, column=0, padx=5, pady=5)
num = tk.Entry(root)
num.grid(row=3, column=1, padx=5, pady=5)

num_passengers_label = tk.Label(root, text="1.標準座 2.商務座 3.自由座: ")
num_passengers_label.grid(row=4, column=0, padx=5, pady=5)
choise = tk.Entry(root)
choise.grid(row=4, column=1, padx=5, pady=5)

num_passengers_label = tk.Label(root, text="是否接受另一種位置 (1是,2否):")
num_passengers_label.grid(row=5, column=0, padx=5, pady=5)
choise2 = tk.Entry(root)
choise2.grid(row=5, column=1, padx=5, pady=5)

confirm_button = tk.Button(root, text="確認", command=lambda: calculate_fare(station, endstation, people, num, choise, choise2))
confirm_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

result_text = tk.Text(root, height=10, width=50)
result_text.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
