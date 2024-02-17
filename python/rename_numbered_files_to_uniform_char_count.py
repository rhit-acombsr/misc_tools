import os
from tkinter import filedialog

def rename_files_in_directory(directory_path):
    # List all files in the directory
    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    
    # Filter files to match specific naming pattern and extract numbers
    filtered_files_and_numbers = [(f, int(f.split('_')[-1].split('.')[0])) for f in files if f.startswith('domain_coloring_') and f.endswith('.png')]
    
    if not filtered_files_and_numbers:
        print("No files found matching the specified pattern.")
        return
    
    # Find the maximum number length
    max_length = max(len(str(num)) for _, num in filtered_files_and_numbers)
    
    # Rename files
    for file_name, number in filtered_files_and_numbers:
        # Generate new file name with the correct number of leading zeros
        new_number_str = str(number).zfill(max_length)
        new_file_name = f"domain_coloring_{new_number_str}.png"
        # Rename file
        os.rename(os.path.join(directory_path, file_name), os.path.join(directory_path, new_file_name))
        print(f"Renamed '{file_name}' to '{new_file_name}'")

# Usage
# directory_path = 'path/to/your/directory'
# rename_files_in_directory(directory_path)

folder_path = filedialog.askdirectory(title="Select Folder:")
rename_files_in_directory(folder_path)