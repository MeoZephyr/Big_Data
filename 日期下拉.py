# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 15:11:05 2024

@author: r0978
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

def next_date(date):
    return date + timedelta(days=1)

def generate_date_list(start_date, end_date):
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date)
        current_date = next_date(current_date)
    return date_list

def submit_selection():
    location1 = location1_combobox.get()
    location2 = location2_combobox.get()
    date = date_combobox.get()
    result_label.config(text=f"你選擇了地點1: {location1}, 地點2: {location2}, 日期: {date}")

# 創建主視窗
root = tk.Tk()
root.title("選擇地點、日期和時間")


# 添加地點1下拉式選單
location1_label = ttk.Label(root, text="地點1:")
location1_label.grid(row=0, column=0, padx=5, pady=5)
location1_combobox = ttk.Combobox(root, values=["南港", "台北", "板橋", "桃園", "新竹", 
                                                "苗栗", "台中", "彰化", "雲林", "嘉義", "台南", "左營"])

location1_combobox.grid(row=0, column=1, padx=5, pady=5)


# 添加地點2下拉式選單
location2_label = ttk.Label(root, text="地點2:")
location2_label.grid(row=1, column=0, padx=5, pady=5)
location2_combobox = ttk.Combobox(root, values=["南港", "台北", "板橋", "桃園", "新竹",
                                                "苗栗", "台中", "彰化", "雲林", "嘉義", "台南", "左營"])
location2_combobox.grid(row=1, column=1, padx=5, pady=5)


# 添加日期下拉式選單，範圍為今天到未來一個月內
start_date = datetime.now().date()
end_date = start_date + timedelta(days=30)
date_list = generate_date_list(start_date, end_date)
date_combobox = ttk.Combobox(root, values=date_list)
date_combobox.grid(row=2, column=1, padx=5, pady=5)


# 添加提交按鈕
submit_button = ttk.Button(root, text="提交", command=submit_selection)
submit_button.grid(row=3, columnspan=2, padx=5, pady=10)


# 添加顯示結果的標籤
result_label = ttk.Label(root, text="")
result_label.grid(row=4, columnspan=2, padx=5, pady=10)

root.mainloop()
