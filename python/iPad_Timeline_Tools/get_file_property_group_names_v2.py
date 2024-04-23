import os
import sys
import win32api
import win32con
import win32com.client

import tkinter as tk
from tkinter import filedialog

def get_file_metadata_groups(path):
    # Normalize the file path to use backslashes
    normalized_path = os.path.normpath(path)

    # Access the shell application object
    shell = win32com.client.Dispatch("Shell.Application")
    namespace = shell.NameSpace(os.path.dirname(normalized_path))

    # Check if the namespace was retrieved successfully
    if not namespace:
        return "Directory not found."

    item = namespace.ParseName(os.path.basename(normalized_path))

    # Check if the item was retrieved successfully
    if not item:
        return "File not found."

    # Set to store unique group names
    group_names = set()

    # Try a safer method to determine the number of details available
    detail_count = 0
    while namespace.GetDetailsOf(namespace.Items(), detail_count):
        detail_count += 1

    # Iterate through property groups and values
    for key in range(detail_count):
        prop_name = namespace.GetDetailsOf(namespace.Items(), key)
        if prop_name:  # Ensure we only add properties with values
            group_name, _ = prop_name.split('\t') if '\t' in prop_name else ("General", prop_name)
            group_names.add(group_name)
    
    return list(group_names)

# Example usage
# file_path = r'C:\Users\acombsr\OneDrive - Rose-Hulman Institute of Technology\Desktop\Lab 4-Depositing Metal Actuators with Electron-Beam Evaporation\Media\Images\audio_metadata.csv'
file_path = filedialog.askopenfilename()
print("file_path = "+file_path)
groups = get_file_metadata_groups(file_path)
print(groups)