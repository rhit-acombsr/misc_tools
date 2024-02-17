from tkinter import filedialog
from PIL import Image
from os import listdir
from os.path import isfile, join, dirname

folder_path = filedialog.askdirectory(title="Select Folder:")
frame_names = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]
frame_names.sort()
frames = []
for frame_name in frame_names:
    frames.append(Image.open(join(folder_path, frame_name)))
output_name = filedialog.asksaveasfile(mode='w',defaultextension=".gif", initialdir=dirname(folder_path),initialfile=folder_path+'.gif').name
frames[0].save(output_name, save_all=True, append_images=frames[1:], optimize=False, duration=0, loop=0)

print("done")
