import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry

def on_city1_select(event=None):
    selected_city1 = city1_var.get()
    update_display(selected_city1, None)
    update_city2_dropdown(selected_city1)

def on_city2_select(event=None):
    selected_city2 = city2_var.get()
    update_display(None, selected_city2)
    update_city1_dropdown(selected_city2)

def on_date_select(event=None):
    selected_date = date_entry.get()
    update_display(None, selected_date)

def update_display(selected_city1, selected_city2):
    display_text.delete(1.0, tk.END)
    if selected_city1:
        display_text.insert(tk.END, f"Selected City 1: {selected_city1}\n")
    if selected_city2:
        display_text.insert(tk.END, f"Selected City 2: {selected_city2}\n")
    if selected_date:
        display_text.insert(tk.END, f"Selected Date: {selected_date}")

root = tk.Tk()
root.title("City and Date Selector")
root.geometry("1000x1000")

cities = ["南港", "台北", "板橋", "桃園", "新竹", "苗栗", "台中", "彰化", "雲林", "嘉義", "台南", "左營"]

# City dropdown menu 1
city1_frame = tk.Frame(root)
city1_frame.pack(side="top", padx=10, pady=10, anchor="nw")

city1_label = tk.Label(city1_frame, text="Select City 1:")
city1_label.pack(side="top", pady=(0, 5))

city1_var = tk.StringVar()
city1_dropdown = ttk.Combobox(city1_frame, textvariable=city1_var, values=cities, width=20)
city1_dropdown.pack(side="top")
city1_dropdown.bind("<<ComboboxSelected>>", on_city1_select)

# City dropdown menu 2
city2_frame = tk.Frame(root)
city2_frame.pack(side="top", padx=10, pady=10, anchor="nw")

city2_label = tk.Label(city2_frame, text="Select City 2:")
city2_label.pack(side="top", pady=(0, 5))

city2_var = tk.StringVar()
city2_dropdown = ttk.Combobox(city2_frame, textvariable=city2_var, values=cities, width=20)
city2_dropdown.pack(side="top")
city2_dropdown.bind("<<ComboboxSelected>>", on_city2_select)

# Date selection
date_frame = tk.Frame(root)
date_frame.pack(side="top", padx=10, pady=10, anchor="nw")

date_label = tk.Label(date_frame, text="Select Date:")
date_label.pack(side="top", pady=(0, 5))

date_entry = DateEntry(date_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
date_entry.pack(side="top")
date_entry.bind("<<DateEntrySelected>>", on_date_select)

# Display selected city and date
display_frame = tk.Frame(root)
display_frame.pack(side="right", padx=10, pady=10)

display_text = tk.Text(display_frame, height=5, width=30)
display_text.pack()

root.mainloop()
