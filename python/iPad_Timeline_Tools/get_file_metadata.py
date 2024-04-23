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

    # Dictionary to hold property groups and their key/values
    metadata = {}

    # Try a safer method to determine the number of details available
    detail_count = 0
    while namespace.GetDetailsOf(namespace.Items(), detail_count):
        detail_count += 1

    # Iterate through property groups and values
    for key in range(detail_count):
        prop_name = namespace.GetDetailsOf(namespace.Items(), key)
        if prop_name:
            group, prop = prop_name.split('\t') if '\t' in prop_name else ("General", prop_name)
            value = namespace.GetDetailsOf(item, key)
            if group not in metadata:
                metadata[group] = {}
            metadata[group][prop] = value

    return metadata

# def get_file_metadata(path):
#     # Normalize the file path to use backslashes
#     normalized_path = os.path.normpath(path)

#     # Access the shell application object
#     shell = win32com.client.Dispatch("Shell.Application")
#     namespace = shell.NameSpace(os.path.dirname(normalized_path))

#     # Debugging output
#     print("Normalized Path: ", normalized_path)
#     print("Directory Path: ", os.path.dirname(normalized_path))

#     # Check if the namespace was retrieved successfully
#     if not namespace:
#         return "Directory not found."

#     item = namespace.ParseName(os.path.basename(normalized_path))

#     # Check if the item was retrieved successfully
#     if not item:
#         return "File not found."

#     # Dictionary to hold property groups and their key/values
#     metadata = {}

#     # Iterate through property groups and values
#     for key in range(0, namespace.GetDetailsOf(item, -1)):
#         prop_name = namespace.GetDetailsOf(namespace.Items(), key)
#         if prop_name:
#             group, prop = prop_name.split('\t') if '\t' in prop_name else ("General", prop_name)
#             value = namespace.GetDetailsOf(item, key)
#             if group not in metadata:
#                 metadata[group] = {}
#             metadata[group][prop] = value

#     return metadata


# def get_file_metadata(path):
#     shell = win32com.client.Dispatch("Shell.Application")
#     namespace = shell.NameSpace(os.path.dirname(path))

#     # Ensure the file exists
#     if not namespace:
#         return "Directory not found."

#     item = namespace.ParseName(os.path.basename(path))

#     # Ensure the item exists
#     if not item:
#         return "File not found."

#     # Dictionary to hold property groups and their key/values
#     metadata = {}

#     # Iterate through property groups and values
#     for key in range(0, namespace.GetDetailsOf(item, -1)):
#         prop_name = namespace.GetDetailsOf(namespace.Items(), key)
#         if prop_name:
#             group, prop = prop_name.split('\t') if '\t' in prop_name else ("General", prop_name)
#             value = namespace.GetDetailsOf(item, key)
#             if group not in metadata:
#                 metadata[group] = {}
#             metadata[group][prop] = value

#     return metadata

# Example usage:
# file_path = r'C:\path\to\your\file.ext'
file_path = filedialog.askopenfilename()
print("file_path = "+file_path)
metadata = get_file_metadata(file_path)
print(metadata)
