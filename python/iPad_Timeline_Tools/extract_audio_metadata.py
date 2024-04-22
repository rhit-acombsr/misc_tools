import os
import csv
from datetime import datetime
from mutagen.mp4 import MP4
import tkinter as tk
from tkinter import filedialog

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

        # Extract creation date, assuming '©day' is used for storing creation date in .m4a files
        media_created = audio.tags.get('©day', [''])[0]
        if media_created:
            try:
                # Format date if it's in a recognizable format
                media_created = datetime.strptime(media_created, '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y %I:%M %p')
            except ValueError:
                pass  # Use the date string as is if it's not in the expected format

        csv_data.append([audio_file, length, media_created])

    # Save to CSV
    csv_file_path = os.path.join(folder_path, "audio_metadata.csv")
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(csv_data)

    print(f"CSV file created: {csv_file_path}")

# Example usage:
# folder_path = 'path_to_your_folder'  # Update the folder path to where your files are stored
root = tk.Tk()
root.withdraw()  # to hide the small tk window
folder_path = filedialog.askdirectory(title="Select Folder Containing Media Files")
extract_audio_metadata(folder_path)
