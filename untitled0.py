# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 15:00:25 2024

@author: r0978
"""

import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime, timedelta

def submit_selection():
    location1 = location1_combobox.get()
    location2 = location2_combobox.get()
    date = date_entry.get_date()
    time = f"{hour_var.get()}:{minute_var.get()}"
    result_label.config(text=f"你選擇了地點1: {location1}, 地點2: {location2}, 日期: {date}, 時間: {time}")

# 創建主視窗
root = tk.Tk()
root.title("選擇地點、日期和時間")

# 添加地點1下拉式選單
location1_label = ttk.Label(root, text="地點1:")
location1_label.grid(row=0, column=0, padx=5, pady=5)
location1_combobox = ttk.Combobox(root, values=["南港", "台北", "板橋", "桃園", "新竹", "苗栗", "台中", "彰化", "雲林", "嘉義", "台南", "左營"])
location1_combobox.grid(row=0, column=1, padx=5, pady=5)

# 添加地點2下拉式選單
location2_label = ttk.Label(root, text="地點2:")
location2_label.grid(row=1, column=0, padx=5, pady=5)
location2_combobox = ttk.Combobox(root, values=["南港", "台北", "板橋", "桃園", "新竹", "苗栗", "台中", "彰化", "雲林", "嘉義", "台南", "左營"])
location2_combobox.grid(row=1, column=1, padx=5, pady=5)

# 添加日期選擇器，限制範圍在今天到未來一個月內
min_date = datetime.now()
max_date = datetime.now() + timedelta(days=30)
date_label = ttk.Label(root, text="日期:")
date_label.grid(row=2, column=0, padx=5, pady=5)
date_entry = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2, min_date=min_date, max_date=max_date)
date_entry.grid(row=2, column=1, padx=5, pady=5)

# 添加時間選擇器 - 小時
hour_label = ttk.Label(root, text="小時:")
hour_label.grid(row=3, column=0, padx=5, pady=5)
hour_var = tk.IntVar()
hour_scale = ttk.Scale(root, from_=0, to=23, variable=hour_var, orient="horizontal")
hour_scale.grid(row=3, column=1, padx=5, pady=5)

# 添加時間選擇器 - 分鐘
minute_label = ttk.Label(root, text="分鐘:")
minute_label.grid(row=4, column=0, padx=5, pady=5)
minute_var = tk.IntVar()
minute_scale = ttk.Scale(root, from_=0, to=59, variable=minute_var, orient="horizontal")
minute_scale.grid(row=4, column=1, padx=5, pady=5)

# 添加提交按鈕
submit_button = ttk.Button(root, text="提交", command=submit_selection)
submit_button.grid(row=5, columnspan=2, padx=5, pady=10)

# 添加顯示結果的標籤
result_label = ttk.Label(root, text="")
result_label.grid(row=6, columnspan=2, padx=5, pady=10)

root.mainloop()
