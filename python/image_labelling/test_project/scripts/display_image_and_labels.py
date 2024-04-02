import os
import tkinter as tk
from tkinter import filedialog
import json
from PIL import Image, ImageTk

# Global variables to keep track of the image list and current index
images_and_labels = []
current_index = 0

def load_labels_and_images(json_file_path, base_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    global images_and_labels
    images_and_labels = []
    for entry in data:
        image_path = os.path.join(base_path, os.path.basename(entry['data']['image']))
        labels = entry['annotations'][0]['result'][0]['value']['choices']
        images_and_labels.append((image_path, labels))

def update_image_and_labels(root, img_label, text_label):
    global current_index
    image_path, labels = images_and_labels[current_index]

    # Load and display the new image
    img = Image.open(image_path)
    img = img.resize((250, 250), Image.Resampling.LANCZOS)
    img_photo = ImageTk.PhotoImage(img)
    img_label.configure(image=img_photo)
    img_label.image = img_photo  # Keep a reference

    # Update the labels text
    label_text = "Labels: " + ", ".join(labels)
    text_label.configure(text=label_text)

def next_image(root, img_label, text_label):
    global current_index
    if current_index < len(images_and_labels) - 1:
        current_index += 1
        update_image_and_labels(root, img_label, text_label)

def previous_image(root, img_label, text_label):
    global current_index
    if current_index > 0:
        current_index -= 1
        update_image_and_labels(root, img_label, text_label)

def display_image_and_labels(root):
    # Initial setup for the first image
    img_label = tk.Label(root)
    img_label.pack(side="top", fill="both", expand="yes")

    text_label = tk.Label(root)
    text_label.pack()

    update_image_and_labels(root, img_label, text_label)

    # Navigation buttons
    prev_button = tk.Button(root, text="Previous", command=lambda: previous_image(root, img_label, text_label))
    prev_button.pack(side="left", expand=True)

    next_button = tk.Button(root, text="Next", command=lambda: next_image(root, img_label, text_label))
    next_button.pack(side="right", expand=True)

    root.mainloop()

def main(root):
    root.withdraw()  # Hide the main window for now
    json_file_path = filedialog.askopenfilename(title="Select the JSON file", filetypes=[("JSON files", "*.json")])
    base_path = filedialog.askdirectory(title="Select the base directory for the images")

    if json_file_path and base_path:
        load_labels_and_images(json_file_path, base_path)
        root.deiconify()  # Show the main window
        display_image_and_labels(root)
    else:
        print("No file or base path selected.")

if __name__ == "__main__":
    root = tk.Tk()
    main(root)
