import os
import tkinter as tk
from tkinter import filedialog
import json
from PIL import Image, ImageTk

def load_labels_and_image(json_file_path, base_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    # Assuming the first entry in the JSON data is the one we want to display
    entry = data[0]
    # Prepend the base path to the image path
    image_path = os.path.join(base_path, entry['data']['image'].lstrip('/'))
    labels = entry['annotations'][0]['result'][0]['value']['choices']
    
    return image_path, labels

def display_image_and_labels(image_path, labels):
    root = tk.Tk()
    root.title("Image and Labels Display")
    
    # Load and display the image
    img = Image.open(image_path)
    img = img.resize((250, 250), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel = tk.Label(root, image=img)
    panel.pack(side="top", fill="both", expand="yes")
    
    # Display the labels
    label_text = "Labels: " + ", ".join(labels)
    label = tk.Label(root, text=label_text)
    label.pack()
    
    root.mainloop()

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Ask for the JSON file path
    json_file_path = filedialog.askopenfilename(title="Select the JSON file", filetypes=[("JSON files", "*.json")])
    # Ask for the base path to the images directory
    base_path = filedialog.askdirectory(title="Select the base directory for the images")
    
    if json_file_path and base_path:
        image_path, labels = load_labels_and_image(json_file_path, base_path)
        display_image_and_labels(image_path, labels)
    else:
        print("No file or base path selected.")

main()
