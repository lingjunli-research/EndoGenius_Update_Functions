from os.path import exists, basename, splitext, dirname, abspath, join
import tkinter as tk
from tkinter import ttk, filedialog, Frame, Button, Label
import subprocess
import time

def select_input_file(canvas):
    input_file=filedialog.askopenfilename(filetypes=[('RAW Files', '*.RAW')])
    global show_on_gui
    if input_file !='':
        try:
            show_on_gui.grid_remove()
        except:
            pass
        output_path=dirname(abspath(input_file))
        file_name=splitext(basename(input_file))[0]
        show_on_gui=Label(canvas, text=file_name, font=('Arial', 10))
        show_on_gui.grid()
    global path_info
    path_info=[input_file, output_path, file_name]

def output_file_info():
    output_file=join(path_info[1], path_info[2])+'.ms2'
    return output_file

def convert(canvas):
    subprocess.run(f'msconvert {path_info[0]} --ms2 -o {path_info[1]}',
                     shell=True, check=True, stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT)
    completion=Label(canvas, text='The RAW file has been converted to ms2.',
                     font=('Arial',10))
    completion.grid()
