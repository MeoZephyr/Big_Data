# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 16:04:36 2024

@author: r0978
"""

import tkinter as tk
from tkinter import ttk

def submit_selection():
    location1 = location1_combobox.get()
    location2 = location2_combobox.get()
    location3 = location3_combobox.get()
    result_label.config(text=f"身分: {location1}, 票券: {location2}, 車廂: {location3}")

# 視窗
root = tk.Tk()
root.title("身分，票券，車廂")

# 身分下拉式選單 location1_combobox
location1_label = ttk.Label(root, text="身分:")
#標題定位
location1_label.grid(row=0, column=0, padx=5, pady=5)
#下拉內容
values_dict1 = {
    "1": '一般票(單程票)',
    "2": '來回票',
    "3": '電子票証(悠遊卡/一卡通)',
    "4": '回數票',
    "5": '定期票(30天期)',
    "6": '定期票(60天期)',
    "7": '早鳥票',
    "8": '團體票'
}
#按照values_dict1內容顯示選單
location1_combobox = ttk.Combobox(root, values=list(values_dict1.values()))
#下拉式選單定位
location1_combobox.grid(row=0, column=1, padx=5, pady=5)


# 票券下拉式選單 location2_label
location2_label = ttk.Label(root, text="票券:")
#標題定位
location2_label.grid(row=1, column=0, padx=5, pady=5)
#下拉內容
values_dict2 = {
    "1":'成人',
    "2":'學生',
    "3":'孩童',
    "4":'敬老',
    "5":'愛心',
    "6":'愛心孩童',
    "7":'愛心優待/愛心陪伴',
    "8":'軍警',
    "9":'法優'
}
#按照values_dict2內容顯示選單
location2_combobox = ttk.Combobox(root, values=list(values_dict2.values()))
#下拉式選單定位
location2_combobox.grid(row=1, column=1, padx=5, pady=5)


# 車廂下拉式選單 location3_label
location3_label = ttk.Label(root, text="車廂:")
#標題定位
location3_label.grid(row=2, column=0, padx=5, pady=5)
#下拉內容
values_dict3 = {
    "1":'標準座車廂',
    "2":'商務座車廂',
    "3":'自由座車廂'
}
#按照values_dict3內容顯示選單
location3_combobox = ttk.Combobox(root, values=list(values_dict3.values()))
#下拉式選單定位
location3_combobox.grid(row=2, column=1, padx=5, pady=5)



#確認按鈕
submit_button = ttk.Button(root, text="確認", command=submit_selection)
#按鈕定位
submit_button.grid(row=3, columnspan=2, padx=5, pady=10)

#顯示結果
result_label = ttk.Label(root, text="")
#顯示定位
result_label.grid(row=4, columnspan=2, padx=5, pady=10)

root.mainloop()