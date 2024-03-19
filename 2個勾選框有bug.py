import tkinter as tk

def toggle_checkbox():
    if var1.get() == 1:
        checkbox2.config(state=tk.DISABLED)
        var2.set(0)  # 确保第二个复选框取消选中
    else:
        checkbox2.config(state=tk.NORMAL)

root = tk.Tk()
root.title("Checkbox Example")

var1 = tk.IntVar()
checkbox1 = tk.Checkbutton(root, text="Checkbox 1", variable=var1, command=toggle_checkbox)
checkbox1.pack()

var2 = tk.IntVar()
checkbox2 = tk.Checkbutton(root, text="Checkbox 2", variable=var2)
checkbox2.pack()

root.mainloop()
