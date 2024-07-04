import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinter import ttk


# Function to read the log file and return its content
def read_log_file(filepath):
    with open(filepath, 'r') as file:
        return file.read()


def log_file_viewer(log_file_path):
    try:
        # Read the log file
        log_content = read_log_file(log_file_path)

        # Create the main application window
        root = tk.Tk()
        root.title("Log Viewer")
        root.geometry("800x600")

        # Apply a modern theme
        style = ttk.Style()
        style.theme_use('clam')

        # Create a frame for better organization
        frame = ttk.Frame(root, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        # Create a ScrolledText widget
        text_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=20)
        text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Insert the log content into the Text widget
        text_area.insert(tk.INSERT, log_content)

        # Make the Text widget read-only
        text_area.configure(state='disabled')

        # Run the Tkinter event loop
        root.mainloop()
    except FileNotFoundError:
        messagebox.showerror("Error", f"Log file '{log_file_path}' not found.")


def choose_log_file():
    # Create a main window for file selection
    choose_window = tk.Tk()
    choose_window.title("Choose Log File")
    choose_window.geometry("300x150")

    # Apply a modern theme
    style = ttk.Style()
    style.theme_use('clam')

    # Create a frame for better organization
    frame = ttk.Frame(choose_window, padding="10")
    frame.pack(fill=tk.BOTH, expand=True)

    # Function to handle button click
    def view_log(log_file):
        choose_window.destroy()
        log_file_viewer(log_file)

    # Button for admin log
    admin_button = ttk.Button(frame, text="Admin Log", command=lambda: view_log('admin.log'))
    admin_button.pack(pady=10, fill=tk.X)

    # Button for facereq log
    facereq_button = ttk.Button(frame, text="Facereq Log", command=lambda: view_log('facereq.log'))
    facereq_button.pack(pady=10, fill=tk.X)

    # Run the Tkinter event loop for the file selection window
    choose_window.mainloop()




