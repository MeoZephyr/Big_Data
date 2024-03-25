from data import Data
import TDX_GeneralTimetable

def get_seat_info(start_station, end_station):
    date = input("輸入日期(格式:yyyy-mm-dd):")
    seat_data = Data().get_AvailableSeat_Status_By_Date(date)
    seats = []
    seat_status = {'O': '尚有座位', 'L': '座位有限', 'X': '已無座位'}
    for jj in seat_data["AvailableSeats"]:
        if jj["OriginStationName"]["Zh_tw"] == start_station and jj["DestinationStationName"]["Zh_tw"] == end_station:
            direction = "北上" if jj["Direction"] == 1 else "南下"
            seat = {
                "direction": direction,
                "train_no": jj["TrainNo"],
                "standard_seat_status": seat_status[jj["StandardSeatStatus"]],
                "business_seat_status": seat_status[jj["BusinessSeatStatus"]]
            }
            seats.append(seat)
    print_seat_info(seats)
    print("取得時刻表")
    TDX_GeneralTimetable.GTT().print_table()

def print_seat_info(seats):
    for seat in seats:
        print("\n" + seat["direction"])
        print("車次:", seat["train_no"])
        print("標準座:", seat["standard_seat_status"])
        print("商務座:", seat["business_seat_status"])
        print("\n-------------------------------------------------")
