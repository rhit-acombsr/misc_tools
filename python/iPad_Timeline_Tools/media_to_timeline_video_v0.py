import os
import csv
import re
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
import hachoir
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from mutagen.mp4 import MP4
from pillow_heif import register_heif_opener
from PIL import Image

def extract_time_taken(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == '.heic':
        try:
            # Use file system's modification time for HEIC files
            file_stat = os.stat(file_path)
            print(file_stat.st_mtime)
            return datetime.fromtimestamp(file_stat.st_mtime).strftime("%I:%M:%S %p")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return '-'
    print("No valid time-taken found for file at path \""+file_path+"\"")
    return '-'

def process_images(folder_path):
    files = [f for f in os.listdir(folder_path) if re.match(r'IMG_\d+\.heic$', f, re.IGNORECASE)]
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

    csv_file_path = os.path.join(folder_path, "images_output.csv")
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(csv_data)

    print(f"CSV file created: {csv_file_path}")

def extract_video_metadata(file_path):
    try:
        parser = createParser(file_path)
        if not parser:
            return '-', '-'
        metadata = extractMetadata(parser)
        if metadata:
            # Properly handle duration if it's present
            if metadata.has('duration'):
                total_seconds = int(metadata.get('duration').seconds)
                # Format duration as H:MM:SS
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                duration = f"{hours}:{minutes:02}:{seconds:02}"
            else:
                duration = '-'

            # Extract creation date and format it
            # creation_date = metadata.get('creation_date').strftime("%I:%M:%S %p") if metadata.has('creation_date') else '-'
            creation_date = metadata.get('creation_date') if metadata.has('creation_date') else '-'
            return creation_date, duration
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return '-', '-'

def process_videos(folder_path):
    files = [f for f in os.listdir(folder_path) if f.lower().endswith('.mov')]
    files.sort()
    video_numbers = {int(f.split('_')[1].split('.')[0]): os.path.join(folder_path, f) for f in files}

    max_num = max(video_numbers.keys(), default=0)
    min_num = min(video_numbers.keys(), default=0)

    csv_data = [["IMG_", "Time Taken", "Length"]]
    for i in range(min_num, max_num + 1):
        if i in video_numbers:
            time_taken, length = extract_video_metadata(video_numbers[i])
            csv_data.append([i, time_taken, length])
        else:
            csv_data.append([i, '-', '-'])

    csv_file_path = os.path.join(folder_path, "videos_output.csv")
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(csv_data)

    print(f"CSV file created: {csv_file_path}")

def convert_heic_to_png(heic_folder_path):
    files = [f for f in os.listdir(heic_folder_path) if f.lower().endswith('.heic')]
    register_heif_opener()
    for filename in files:
        heic_path = os.path.join(heic_folder_path, filename)
        png_path = os.path.join(heic_folder_path, filename[:-5] + '.png')

        # Check if the PNG version already exists
        if not os.path.exists(png_path):
            try:
                # Open HEIC file
                with Image.open(heic_path) as img:
                    # Convert HEIC to PNG
                    img.save(png_path, "PNG")
                    print(f"Converted {filename} to PNG format.")
            except Exception as e:
                print(f"Failed to convert {filename}: {e}")
        else:
            print(f"Skipping conversion for {filename} as PNG version already exists.")

def format_duration(seconds):
    # Convert duration in seconds to HH:MM:SS format
    return str(datetime.utcfromtimestamp(seconds).strftime('%H:%M:%S'))

def extract_audio_metadata(folder_path):
    audio_files = [f for f in os.listdir(folder_path) if f.endswith('.m4a')]
    csv_data = [["Audio File Name", "Length", "Media Created"]]

    for audio_file in audio_files:
        full_path = os.path.join(folder_path, audio_file)
        audio = MP4(full_path)

        # Extract duration and format it
        length = format_duration(audio.info.length)

        # Attempt to extract the creation date
        media_created = audio.tags.get('©day', None)
        if media_created is None:
            raise ValueError(f"No 'Media Created' metadata found for file {audio_file}")

        try:
            # Try to format the 'Media Created' date
            media_created = datetime.strptime(media_created[0], '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y %I:%M %p')
        except ValueError as e:
            raise ValueError(f"Date format error in file {audio_file}: {e}")

        csv_data.append([audio_file, length, media_created])

    # Save to CSV
    csv_file_path = os.path.join(folder_path, "audio_metadata.csv")
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(csv_data)

    print(f"CSV file created: {csv_file_path}")

def consolidate_media_metadata(media_folder_path):
    # Process each media type
    process_images(media_folder_path)
    process_videos(media_folder_path)
    convert_heic_to_png(media_folder_path)
    extract_audio_metadata(media_folder_path)
    
    # Initialize a dictionary to hold all metadata
    all_media_metadata = {
        'images': [],
        'videos': [],
        'audio': []
    }
    
    # Read metadata from CSV files
    # Images
    images_csv_path = os.path.join(media_folder_path, "images_output.csv")
    with open(images_csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            all_media_metadata['images'].append(row)

    # Videos
    videos_csv_path = os.path.join(media_folder_path, "videos_output.csv")
    with open(videos_csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            all_media_metadata['videos'].append(row)

    # Audio
    audio_csv_path = os.path.join(media_folder_path, "audio_metadata.csv")
    with open(audio_csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            all_media_metadata['audio'].append(row)

    return all_media_metadata

import tkinter as tk

def display_basic_timeline():
    # Create the main window
    root = tk.Tk()
    root.title("Media Timeline")
    
    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Set the size of the window to full screen
    root.geometry(f"{screen_width}x{screen_height}")
    
    # Create a canvas for drawing the timeline
    canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg='white')
    canvas.pack(fill=tk.BOTH, expand=True)
    
    # Draw a central horizontal line across the screen
    line_y = screen_height // 2
    canvas.create_line(0, line_y, screen_width, line_y, fill='black', width=2)
    
    # Start the Tkinter event loop
    root.mainloop()

# # Example usage:
# # Set up to use a GUI for folder selection
# root = tk.Tk()
# root.withdraw()  # to hide the small tk window
# folder_path = filedialog.askdirectory(title="Select Folder Containing Video Files")
# process_videos(folder_path)

# # Example usage:
# # Set up to use a GUI for folder selection
# root = tk.Tk()
# root.withdraw()  # to hide the small tk window
# folder_path = filedialog.askdirectory(title="Select Folder Containing Image Files")
# process_images(folder_path)

# # Example usage:
# # Assuming you have a directory picker or you can specify the path directly
# root = tk.Tk()
# root.withdraw()  # to hide the small tk window
# heic_folder_path = filedialog.askdirectory(title="Select Folder Containing HEIC Images")
# convert_heic_to_png(heic_folder_path)

# Example usage:
# folder_path = 'path_to_your_folder'  # Update the folder path to where your files are stored
# root = tk.Tk()
# root.withdraw()  # to hide the small tk window
# folder_path = filedialog.askdirectory(title="Select Folder Containing Media Files")
# extract_audio_metadata(folder_path)

# Example usage:
# Set up to use a GUI for folder selection
root = tk.Tk()
root.withdraw()  # to hide the small tk window
media_folder_path = filedialog.askdirectory(title="Select Folder Containing All Media Files")
metadata = consolidate_media_metadata(media_folder_path)
print(metadata)

# # Example usage
# display_basic_timeline()
