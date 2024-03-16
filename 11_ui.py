import requests
from tkinter import *

app_id = 'B11002064-0b185a9c-e5b5-4196'
app_key = 'd2da45c3-9a9e-47f2-9b1d-68885bcc08ee'
auth_url = "https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"
url = "https://tdx.transportdata.tw/api/basic/v2/Rail/THSR/AvailableSeatStatusList?%24top=30&%24format=JSON"


class Auth():
    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key

    def get_auth_header(self):
        content_type = 'application/x-www-form-urlencoded'
        grant_type = 'client_credentials'

        return {
            'content-type': content_type,
            'grant_type': grant_type,
            'client_id': self.app_id,
            'client_secret': self.app_key
        }


class Data():
    def __init__(self, auth_response):
        self.auth_response = auth_response

    def get_data_header(self):
        auth_json = self.auth_response.json()
        access_token = auth_json.get('access_token')

        return {
            'authorization': 'Bearer ' + access_token
        }


def fetch_data(station):
    try:
        data_response = requests.get(url, headers=data.get_data_header())
        available_seats = data_response.json()["AvailableSeats"]
        output_text.delete(1.0, END)  # Clear previous content
        for j in available_seats:
            if j["StationName"]["Zh_tw"] == station:
                if j["Direction"] == 1:
                    output_text.insert(END, "\n北上\n")
                else:
                    output_text.insert(END, "\n南下\n")
                output_text.insert(END, "車次: " + str(j["TrainNo"]) + "\n")
                for i in j["StopStations"]:
                    output_text.insert(END, j["StationName"]["Zh_tw"] + " - " + i["StationName"]["Zh_tw"] + "\n")
                    if i["StandardSeatStatus"] == "O":
                        output_text.insert(END, "標準座: 尚有座位\n")
                    elif i["StandardSeatStatus"] == "L":
                        output_text.insert(END, "標準座: 座位有限\n")
                    else:
                        output_text.insert(END, "標準座: 已無座位\n")
                    if i["BusinessSeatStatus"] == "O":
                        output_text.insert(END, "商務艙: 尚有座位\n")
                    elif i["BusinessSeatStatus"] == "L":
                        output_text.insert(END, "商務艙: 座位有限\n")
                    else:
                        output_text.insert(END, "商務艙: 已無座位\n")
                output_text.insert(END, "-------------------------------------------------\n")
    except Exception as e:
        print("An error occurred:", e)


def search():
    station = entry_station.get()
    fetch_data(station)


# Authenticate
auth = Auth(app_id, app_key)
auth_response = requests.post(auth_url, auth.get_auth_header())

# Create Data object
data = Data(auth_response)

# Tkinter GUI
root = Tk()
root.geometry("1000x1000")
root.configure(bg='white')

label_station = Label(root, text="輸入車站:", bg="white")
label_station.pack()

entry_station = Entry(root, width=30)
entry_station.pack()

button_search = Button(root, text="Search", command=search)
button_search.pack()

output_text = Text(root, height=40, width=50)
output_text.pack()

root.mainloop()
