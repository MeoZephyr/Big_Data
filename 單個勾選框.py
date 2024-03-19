# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 22:27:33 2024

@author: r0978
"""

import tkinter as tk

def toggle_checkbox():
    if var.get() == 1:
        label.config(text="Checkbox is checked")
    else:
        label.config(text="Checkbox is unchecked")

root = tk.Tk()
root.title("Checkbox Example")

var = tk.IntVar()
checkbox = tk.Checkbutton(root, text="Check me", variable=var, command=toggle_checkbox)
checkbox.pack()

label = tk.Label(root, text="Checkbox is unchecked")
label.pack()

root.mainloop()
