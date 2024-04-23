import os
import sys
import win32api
import win32con
import win32com.client

import tkinter as tk
from tkinter import filedialog

def get_file_metadata(path):
    # Normalize the file path to use backslashes
    normalized_path = os.path.normpath(path)

    # Access the shell application object
    shell = win32com.client.Dispatch("Shell.Application")
    namespace = shell.NameSpace(os.path.dirname(normalized_path))

    # Debugging output
    print("Normalized Path: ", normalized_path)
    print("Directory Path: ", os.path.dirname(normalized_path))

    # Check if the namespace was retrieved successfully
    if not namespace:
        return "Directory not found."

    item = namespace.ParseName(os.path.basename(normalized_path))

    # Check if the item was retrieved successfully
    if not item:
        return "File not found."

    # List to hold property groups and their properties
    metadata = []

    # Try a safer method to determine the number of details available
    detail_count = 0
    while namespace.GetDetailsOf(namespace.Items(), detail_count):
        detail_count += 1

    # Group names could be repeated, we need to ensure they are captured uniquely
    groups = {}

    # Iterate through property groups and values
    for key in range(detail_count):
        prop_name = namespace.GetDetailsOf(namespace.Items(), key)
        prop_value = namespace.GetDetailsOf(item, key)
        if prop_name and prop_value:  # Ensure we only add properties with values
            group, prop = prop_name.split('\t') if '\t' in prop_name else ("General", prop_name)
            if group not in groups:
                groups[group] = []
            groups[group].append((prop, prop_value))
    
    # Convert groups dictionary to list of tuples
    for group, properties in groups.items():
        metadata.append((group, properties))

    return metadata

# Example usage:
# file_path = r'C:\path\to\your\file.ext'
file_path = filedialog.askopenfilename()
print("file_path = "+file_path)
metadata = get_file_metadata(file_path)
print(metadata)
