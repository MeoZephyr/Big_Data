import requests
import json
from data import Data
list1=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

class GTT():
    def print_table(self):
        json_data = Data().get_GeneralTime_table()
        for j in range(len(json_data)):
            print("--------------------------------------------------")
            print("生效期間:",end=" ")
            print(json_data[j]["EffectiveDate"],"~",json_data[j]["ExpiringDate"])
            print("列車ID: ",json_data[j]["GeneralTimetable"]["GeneralTrainInfo"]["TrainNo"])
            print("停靠站: ",end=" ")

            for i in range(len(json_data[j]["GeneralTimetable"]["StopTimes"])):
                print(json_data[j]["GeneralTimetable"]["StopTimes"][i]["StationName"]["Zh_tw"],end=" -> ")
            print("end!")

            print("到站時間與出發時間")
            print("時間表:",end=" ")
            for i in range(len(json_data[j]["GeneralTimetable"]["StopTimes"])):
                if i ==0:
                    print(json_data[j]["GeneralTimetable"]["StopTimes"][i]["DepartureTime"],end=" -> ") 
                    continue
                if i==len(json_data[j]["GeneralTimetable"]["StopTimes"])-1:
                    print(json_data[j]["GeneralTimetable"]["StopTimes"][i]["ArrivalTime"],end=" -> ") 
                    continue
                print(json_data[j]["GeneralTimetable"]["StopTimes"][i]["DepartureTime"],end=" -> ")
            print("end!")

            print("行駛日 -> ",end=" ")
            for i in list1:
                if json_data[j]["GeneralTimetable"]["ServiceDay"][i]==1:
                    print(i,end=" ")
            print()
            print("--------------------------------------------------")

