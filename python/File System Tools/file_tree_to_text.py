import os
import tkinter as tk
from tkinter import filedialog

def generate_directory_tree(directory: str, indent: str = "", is_last: bool = True) -> str:
    """Generates a human-readable tree representation of a directory."""
    tree_str = ""
    items = sorted(os.listdir(directory))
    
    for index, item in enumerate(items):
        path = os.path.join(directory, item)
        is_dir = os.path.isdir(path)
        connector = "└── " if index == len(items) - 1 else "├── "
        
        tree_str += f"{indent}{connector}{item}\n"
        
        if is_dir:
            new_indent = indent + ("    " if index == len(items) - 1 else "│   ")
            tree_str += generate_directory_tree(path, new_indent, index == len(items) - 1)
    
    return tree_str

def print_directory_tree(directory: str):
    """Prints the directory tree starting from the given directory."""
    print(directory)
    print(generate_directory_tree(directory))

def select_directory_and_print_tree():
    """Opens a Tkinter folder selection dialog and prints the directory tree."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    directory = filedialog.askdirectory()
    if directory:
        print_directory_tree(directory)

# Example usage:
select_directory_and_print_tree()
