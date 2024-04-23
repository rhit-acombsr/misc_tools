import os
import sys
import win32api
import win32con
import win32com.client

import tkinter as tk
from tkinter import filedialog

def get_property_group_names(path):
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

    # Set to hold unique group names
    group_names = set()

    # Get number of details available
    detail_count = namespace.GetDetailsOf(item, -1)

    # Iterate over each property and extract group names
    for index in range(detail_count):
        prop_name = namespace.GetDetailsOf(namespace.Items(), index)
        if prop_name:
            group = prop_name.split('\t')[0] if '\t' in prop_name else "General"
            group_names.add(group)

    return list(group_names)

# Example usage
# file_path = r'C:\path\to\your\file.ext'
file_path = filedialog.askopenfilename()
print("file_path = "+file_path)
group_names = get_property_group_names(file_path)
print(group_names)
