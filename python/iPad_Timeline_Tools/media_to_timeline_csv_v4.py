import os
import csv
import re
from datetime import datetime
import tkinter as tk
from tkinter import filedialog

def extract_time_taken(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    try:
        # Use file system's modification time for HEIC files
        if ext == '.heic':
            file_stat = os.stat(file_path)
            return datetime.fromtimestamp(file_stat.st_mtime).strftime("%I:%M:%S %p")
        elif ext in ['.jpeg', '.jpg', '.png']:
            from PIL import Image
            img = Image.open(file_path)
            metadata = img.getexif()
            time_taken = metadata.get(36867)  # DateTimeOriginal
            if time_taken:
                return datetime.strptime(time_taken, "%Y:%m:%d %H:%M:%S").strftime("%I:%M:%S %p")
        else:
            from hachoir.parser import createParser
            from hachoir.metadata import extractMetadata
            parser = createParser(file_path)
            if not parser:
                return '-'
            with parser:
                metadata = extractMetadata(parser)
            if metadata and 'creation_date' in metadata.exportDictionary():
                return metadata.get('creation_date').strftime("%I:%M:%S %p")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    return '-'

def process_images_and_videos(folder_path):
    files = [f for f in os.listdir(folder_path) if re.match(r'IMG_\d+\.(jpeg|jpg|png|heic|mov|mp4)$', f, re.IGNORECASE)]
    files.sort()
    image_numbers = {int(f.split('_')[1].split('.')[0]): os.path.join(folder_path, f) for f in files}

    max_num = max(image_numbers.keys(), default=0)
    min_num = min(image_numbers.keys(), default=0)

    csv_data = [["IMG_", "Time Taken"]]
    for i in range(min_num, max_num + 1):
        if i in image_numbers:
            time_taken = extract_time_taken(image_numbers[i])
            csv_data.append([i, time_taken])
        else:
            csv_data.append([i, '-'])

    csv_file_path = os.path.join(folder_path, "output.csv")
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(csv_data)

    print(f"CSV file created: {csv_file_path}")

# Example usage:
# folder_path = 'path_to_your_folder'  # Update the folder path to where your files are stored
root = tk.Tk()
root.withdraw()  # to hide the small tk window
folder_path = filedialog.askdirectory(title="Select Folder Containing Media Files")
process_images_and_videos(folder_path)
