import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Function to open a file dialog and get the CSV file path
def open_csv_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        # Load the CSV file into a pandas DataFrame
        df = pd.read_csv(file_path)

        # Check if the DataFrame has exactly 3 columns
        if len(df.columns) != 3:
            print("The selected CSV file must have exactly 3 columns.")
            return

        # Create a 3D scatter plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(df.iloc[:, 0], df.iloc[:, 1], df.iloc[:, 2])

        # Set labels for the axes
        ax.set_xlabel(df.columns[0])
        ax.set_ylabel(df.columns[1])
        ax.set_zlabel(df.columns[2])

        # Show the plot
        plt.show()

# Create the main UI window
root = tk.Tk()
root.title("3D Scatter Plot from CSV")

# Create a button to open the CSV file
open_button = tk.Button(root, text="Open CSV File", command=open_csv_file)
open_button.pack(pady=20)

# Start the UI main loop
root.mainloop()
