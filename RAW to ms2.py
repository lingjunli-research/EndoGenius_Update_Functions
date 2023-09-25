import tkinter as tk
from tkinter import ttk, filedialog, Frame, Label, Button, Listbox
from os.path import normpath
import os
import utility as u

#input_file=r'C:\Users\18918\Downloads\2021_0817_Brain_2.raw'

master=tk.Tk()
master.title('RAW2ms2')
master.geometry('700x700')
input_file_selection=Button(master, text='Select RAW file', font=('Arial', 15),
                            command=lambda: u.select_input_file(master))
input_file_selection.grid()
start_conversion=Button(master, text='Click to convert', font=('Arial', 15),
                        command=lambda: u.convert(master))
start_conversion.place(x=500, y=100)
close=Button(master, text='Click to close GUI', font=('Arial', 15),
             command=lambda: master.destroy())
close.place(x=100, y=600)

master.mainloop()
output_file=u.output_file_info()
output_file_path=normpath(output_file)
print(output_file_path)
