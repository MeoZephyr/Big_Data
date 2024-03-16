import requests,json
from data import Data

class Seat():
    
    def __init__(self) -> None:
        print("Seat init")
#        date = input("輸入日期(格式:yyyy-mm-dd):")
        date = "2024-03-17"
        self.seat_data = Data().get_AvailableSeat_Status_By_Date(date)
        print("end")
#        print(self.seat_data)

#        self.over_view()
 #       self.view_seat()


    def view_seat(self):
        StartStation = input("輸入出發車站:")
        EndStation = input("輸入目的地車站:")

        seat = {'O':'尚有座位','L':'座位有限','X':'已無座位'}
        for jj in self.seat_data["AvailableSeats"]:
                if jj["OriginStationName"]["Zh_tw"] == StartStation and jj["DestinationStationName"]["Zh_tw"] == EndStation:
                    if jj["Direction"]==1:
                        print("\n北上")
                    else:
                        print("\n南下")
                    print("車次:",jj["TrainNo"])
                    print("標準座:",seat[jj["StandardSeatStatus"]])
                    print("商務座:",seat[jj["BusinessSeatStatus"]])
                    print()
                    print("-------------------------------------------------")
        print("end funtion view_seat")
    

