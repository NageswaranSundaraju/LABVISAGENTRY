import tkinter as tk
from tkinter import scrolledtext
import smbclient


smbclient.ClientConfig(username='Nageswaran', password='N@ges2023')

# Function to read the log file and return its content
def read_log_file(filepath):
    with smbclient.open_file(filepath, 'r') as file:
        return file.read()

# Path to the log file
log_file_path = '//192.168.0.254/D/PythonFileTesting/log.txt'

# Read the log file
log_content = read_log_file(log_file_path)

# Create the main application window
root = tk.Tk()
root.title("Log Viewer")

# Create a ScrolledText widget
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Insert the log content into the Text widget
text_area.insert(tk.INSERT, log_content)

# Make the Text widget read-only
text_area.configure(state='disabled')

# Run the Tkinter event loop
root.mainloop()
