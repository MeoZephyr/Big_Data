import requests
import json
from data import Data
list1 = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

class GTT():
    def print_table(self):
        json_data = Data().get_GeneralTime_table()
        tables = []
        for data in json_data:
            table = []
            table.append("--------------------------------------------------")
            table.append(f"生效期間: {data['EffectiveDate']} ~ {data['ExpiringDate']}")
            table.append(f"列車ID: {data['GeneralTimetable']['GeneralTrainInfo']['TrainNo']}")
            table.append("停靠站: " + " -> ".join(stop['StationName']['Zh_tw'] for stop in data['GeneralTimetable']['StopTimes']) + " end!")
            table.append("到站時間與出發時間")
            time_table = "時間表: "
            for i, stop in enumerate(data['GeneralTimetable']['StopTimes']):
                if i == 0:
                    time_table += stop['DepartureTime'] + " -> "
                elif i == len(data['GeneralTimetable']['StopTimes']) - 1:
                    time_table += stop['ArrivalTime'] + " -> "
                else:
                    time_table += stop['DepartureTime'] + " -> "
            table.append(time_table + "end!")
            table.append("行駛日 -> " + " ".join(day for day in list1 if data['GeneralTimetable']['ServiceDay'][day] == 1))
            table.append("--------------------------------------------------")
            tables.append("\n".join(table))
        print("\n".join(tables))
