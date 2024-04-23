from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog
from pillow_heif import register_heif_opener

def convert_heic_to_png(heic_folder_path):
    files = [f for f in os.listdir(heic_folder_path) if f.lower().endswith('.heic')]
    register_heif_opener()
    for filename in files:
        heic_path = os.path.join(heic_folder_path, filename)
        try:
            # Open HEIC file
            with Image.open(heic_path) as img:
                # Convert HEIC to PNG
                png_path = os.path.join(heic_folder_path, filename[:-5] + '.png')
                img.save(png_path, "PNG")
                print(f"Converted {filename} to PNG format.")
        except Exception as e:
            print(f"Failed to convert {filename}: {e}")

# Example usage:
# Assuming you have a directory picker or you can specify the path directly
root = tk.Tk()
root.withdraw()  # to hide the small tk window
heic_folder_path = filedialog.askdirectory(title="Select Folder Containing HEIC Images")
convert_heic_to_png(heic_folder_path)
