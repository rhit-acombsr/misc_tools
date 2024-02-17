import os
from tkinter import filedialog
from os.path import dirname

input_path = filedialog.askopenfilename()
# input_dir = dirname(input_path)
# file_name = input_path[len(input_dir):]
output_dir = filedialog.askdirectory(title="Select Folder:")
# output_path = output_dir + file_name

# os.rename(input_path, output_path)
os.rename(input_path, (output_dir + (input_path[len(dirname(input_path)):])))