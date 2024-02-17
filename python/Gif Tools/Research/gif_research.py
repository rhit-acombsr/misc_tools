from PIL import Image
from PIL.GifImagePlugin import GifImageFile
from PIL import ImageFile
from tkinter import filedialog

filetypes = (("GIF files", "*.gif"), ("All files", "*.*"))
file_name = filedialog.askopenfilename(filetypes=filetypes)
with open(file_name, mode='rb') as file:
    file_content = file.read()
    # print(str(type(file)))
    # print(str(type(file_content)))

# Making a gif:
# frames = []

# Image -> ImageFile -> GifImageFile

imgIn = Image.open(file_name)
print(str(type(imgIn))) # <class 'PIL.GifImagePlugin.GifImageFile'>
# print(imgIn.n_frames) # 3


# img0 = imgIn.seek(0)
# print(str(type(img0))) # <class 'NoneType'>
# print(img0) # None

# img1 = imgIn.seek(imgIn.tell() + 1)
# print(str(type(img1))) #

# for frame in range(imgIn.n_frames):
#     frames[frame] = 
#     print()

# for i in range(imgIn.n_frames):
#     seekval = imgIn.n_frames // imgIn.n_frames * i
#     imgIn.seek(seekval)
#     print(seekval)
#     imgIn.save('{}.png'.format(i))

# print(file_name)
# name = filedialog.asksaveasfile(mode='w',defaultextension=".txt").name
# print(name)
# file_path = filedialog.askopenfilename()
# print(file_path)
# folder_path = filedialog.askdirectory(title="Select Folder:")
# print(folder_path)

# print(str(type(imgIn)))
# gif_image_file = GifImageFile()
# image_file = ImageFile()
# image = Image()

# print("complete")
# print(str(type()))


# import csv

# with open('coors.csv', mode='r') as infile:
#     reader = csv.reader(infile)
#     with open('coors_new.csv', mode='w') as outfile:
#         writer = csv.writer(outfile)
#         mydict = {rows[0]:rows[1] for rows in reader}

