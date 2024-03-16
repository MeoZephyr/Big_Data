# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 21:44:17 2024

@author: r0978
"""

from tkinter import *


root = Tk()
root.title("高鐵查詢") # 視窗標題
root.iconbitmap('icons8-train-80.ico')
root.geometry("1300x1000") # 視窗大小 長x寬
#root.geometry("300x160+400+200") # 距離螢幕左上角(400,200)
#   screenWidth = root.winfo_screenwidth() # 螢幕寬度
#   screenHeight = root.winfo_screenheight()
root.configure(bg='white') # 視窗背景顏色

label = Label(root,text="台 灣 高 鐵", bg = "white", width=100, height=8)
#font="Helvetica 16 bold italic") 16 字型大小 bold, italic: 粗體，斜體

label1 = Label(root,text="起站: ").grid(row=0)
label2 = Label(root,text="終點站: ").grid(row=1)
e1 = Entry(root) # 輸入文字
e2 = Entry(root) # 輸入文字Entry(root, show='*') show * 用*取代輸入顯示文字
e1.grid(row=0,column=1) # 定位輸入文字框
e2.grid(row=1,column=1)



root.mainloop()