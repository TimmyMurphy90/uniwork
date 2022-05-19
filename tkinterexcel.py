import tkinter as from tkinter import 
from tkinter import fieldialog, messagebox, ttk

import pandas as pd

root = tk.tk()
root.geometry("500x500")
root.pack_propagate(false)
root.resizable(0,0)

frame1 = tk.Labelframe(root, text="Excel Data")
frame1.place(height=250,width=500)

file_frame = tk.LabelFrame(root, text="open file")
file_frame.place(height=100, width=400, rely=0.65, relx=0)

button1= tk.Button(file_frame, text="Browse a file")
button1.place(rely=0.65, relx=0.50)

button2 = tk.Button(file_frame, text= "load file")
button2.place(rely=0.65, relx=0.10)

label_file = ttk.Label(file_frame, text="no file selected")
label_file.place(rely=0, relx=0)


tv1 = ttk.Treeview(frame1)
tv1.place(relheight=1,relwidth=1)

treescrolly = tk.Scrollbar(frame1, orient="vertical", command=tv1.yview)
treescrollx= tk.Scrollbar(frame1, orient ="horizontal", command=tv1.xview)
tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)
treescrollx.pack(side="button", fill="x")
treescrolly.pack(side="right", fill="y")


root.mainloop()