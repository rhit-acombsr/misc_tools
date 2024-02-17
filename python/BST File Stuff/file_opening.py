import subprocess
from tkinter import filedialog

test_dir = filedialog.askdirectory(title="Select Folder:")
# print(test_dir)
# test_dir = 'C:/Users/acomb/Desktop/test'

# subprocess.Popen('explorer "C:/Users/acomb/Desktop/test"') #doesn't open correct folder
# subprocess.Popen('explorer')
# subprocess.Popen('explorer "C:\\Users\\acomb\\Desktop\\test"') #works

fixed_dir = test_dir.replace('/','\\')
p_open_args = 'explorer "' + fixed_dir + '"'
subprocess.Popen(p_open_args)

