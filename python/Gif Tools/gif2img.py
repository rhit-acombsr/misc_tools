from tkinter import filedialog
from PIL import Image
from os import mkdir
from os.path import join, dirname

filetypes = (("GIF files", "*.gif"), ("All files", "*.*"))
file_path = filedialog.askopenfilename(filetypes=filetypes)
imgIn = Image.open(file_path)
file_dir = dirname(file_path)
file_name = file_path[len(file_dir)+1:len(file_path)-4]
folder_path = file_dir + '/' + file_name
try:
    mkdir(folder_path)
except OSError as error:
    pass
images_path = folder_path + '/images'
try:
    mkdir(images_path)
except OSError as error:
    pass
with open(folder_path + '/frame_durations.csv', 'w', encoding="utf-8") as f:
    f.write("%s,%s\n"%('frame','duration (s/100)'))
    for i in range(imgIn.n_frames):
        imgIn.seek(imgIn.n_frames // imgIn.n_frames * i)
        imgIn.save(images_path + '/' + str(i) + '.png')
        f.write("%s,%s\n"%(str(i),str(imgIn.info['duration'])))
        
print("done")