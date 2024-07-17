import json
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from threading import Thread
import DeviceStatus
from CaptureFace import capture_images
import TkinterDisplayLog
import train_model
import showlect
import logging

logging.basicConfig(filename='admin.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the JSON configuration file
with open('config.json') as config_file:
    config = json.load(config_file)

# Dark theme colors
background_color = "#2e2e2e"
foreground_color = "#ffffff"
button_color = "#4d4d4d"
highlight_color = "#007acc"

class DataEntryForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("LVE USER DATA FORM")
        self.geometry("400x300")
        self.configure(background=background_color)

        # Apply a dark theme
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background=background_color)
        style.configure("TLabel", background=background_color, foreground=foreground_color)
        style.configure("TEntry", fieldbackground=button_color, foreground=foreground_color)
        style.configure("TButton", background=button_color, foreground=foreground_color, borderwidth=1)
        style.map("TButton", background=[("active", highlight_color)])

        # Fonts
        NORMAL_FONT = ("Arial", 15)

        # Detail Section
        detail_frame = ttk.Frame(self, padding="10")
        detail_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        name_label = ttk.Label(detail_frame, text='NAME', font=NORMAL_FONT)
        name_label.grid(row=0, column=0, pady=10, padx=10, sticky='w')
        noic_label = ttk.Label(detail_frame, text='NO IC', font=NORMAL_FONT)
        noic_label.grid(row=1, column=0, pady=10, padx=10, sticky='w')
        notel_label = ttk.Label(detail_frame, text='NO TEL', font=NORMAL_FONT)
        notel_label.grid(row=2, column=0, pady=10, padx=10, sticky='w')

        self.name_entry = ttk.Entry(detail_frame, font=NORMAL_FONT)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        self.noic_entry = ttk.Entry(detail_frame, font=NORMAL_FONT)
        self.noic_entry.grid(row=1, column=1, padx=10, pady=10, sticky='ew')
        self.notel_entry = ttk.Entry(detail_frame, font=NORMAL_FONT)
        self.notel_entry.grid(row=2, column=1, padx=10, pady=10, sticky='ew')

        detail_frame.columnconfigure(1, weight=1)  # Make entry columns expandable

        self.open_cam_btn = ttk.Button(detail_frame, text='OPEN CAMERA', command=self.open_camera, style='TButton')
        self.open_cam_btn.grid(row=4, column=0, pady=20, columnspan=2, padx=10)

        self.enroll_btn = ttk.Button(detail_frame, text='Enroll Face', command=self.enroll_face, style='TButton', state=tk.DISABLED)
        self.enroll_btn.grid(row=1, column=2, padx=30, pady=10, ipadx=10)

        self.clear_btn = ttk.Button(detail_frame, text='Clear', command=self.clear_entries, style='TButton')
        self.clear_btn.grid(row=2, column=2, padx=30, pady=10, ipadx=20)

        # Add Lorem Ipsum text box
        lorem_text = (
            "Welcome to LVE USER DATA FORM\n\n"
            "HOW TO USE\n\n"
            "Step 1: ADD USER DETAIL\n"
            "Add user's Name, IC Number, and Phone Number\n\n"
            "Step 2: Capture User's Face\n"
            "Click the Open camera button and wait until the camera captures the face\n"
            "After that click the Enroll Face Button to save the user data.\n"
            "Finally close the form and click Train Face to train all the faces\n\n"
        )

        text_box_frame = ttk.Frame(self, padding="10")
        text_box_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        text_box = tk.Text(text_box_frame, wrap=tk.WORD, background=button_color, foreground=foreground_color)
        text_box.insert(tk.END, lorem_text)
        text_box.config(state=tk.DISABLED)  # Make the text box read-only
        text_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def open_camera(self):
        username = self.noic_entry.get()
        if username.strip():
            capture_images(username)
            self.enroll_btn.config(state=tk.NORMAL)
        else:
            messagebox.showwarning("Warning", "Please enter a name before opening the camera.")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.noic_entry.delete(0, tk.END)
        self.notel_entry.delete(0, tk.END)

    def enroll_face(self):
        name = self.name_entry.get()
        noic = self.noic_entry.get()
        notel = self.notel_entry.get()

        if name.strip() and noic.strip() and notel.strip():
            summary = f"Name: {name}\nNo IC: {noic}\nNo Tel: {notel}\n"
            confirm = messagebox.askokcancel("Confirm Data",
                                             f"Please confirm the following data will be added to the database:\n\n"
                                             f"{summary}")
            if confirm:
                try:
                    connection = mysql.connector.connect(
                        user=config["database"]["user"],
                        password=config["database"]["password"],
                        host=config["database"]["host"],
                        database=config["database"]["db"]
                    )
                    cursor = connection.cursor()
                    insert_query = "INSERT INTO lect (noic, name, notel) VALUES (%s, %s, %s)"
                    cursor.execute(insert_query, (noic, name, notel))
                    connection.commit()
                    cursor.close()
                    connection.close()
                    messagebox.showinfo("Success", "Data inserted successfully!")
                    logging.info(f"Data Added Name: {name} NoIC: {noic}")
                    self.clear_entries()
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Error: {err}")
                    logging.error(f"DATABASE ERROR {err}")
        else:
            messagebox.showwarning("Warning", "Please fill in all fields.")

def check_db_connection(label):
    print(label)
    try:
        connection = mysql.connector.connect(
            user=config["database"]["user"],
            password=config["database"]["password"],
            host=config["database"]["host"],
            database=config["database"]["db"]
        )
        print("connecting...")
        connection.close()
        label.config(text="Database Status: Connected", foreground="green")
        print("connected")
    except mysql.connector.Error:
        label.config(text="Database Status: Disconnected", foreground="red")
        print("disconnected")



def update_connection_status_in_thread(label):

    thread = Thread(target=check_db_connection, args=(label,))
    thread.start()
    print("hhhh")


def main():
    root = tk.Tk()
    root.title("LVE ADMIN")
    root.geometry("800x500")
    root.configure(background=background_color)

    # Apply a dark theme
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TFrame", background=background_color)
    style.configure("TLabel", background=background_color, foreground=foreground_color)
    style.configure("TButton", background=button_color, foreground=foreground_color, borderwidth=1)
    style.map("TButton", background=[("active", highlight_color)])
    style.configure("TText", background=button_color, foreground=foreground_color, borderwidth=1)

    # Fonts
    TITLE_FONT = ("Arial", 30, "bold")
    BUTTON_FONT = ("Arial", 12)

    # Header
    header_frame = ttk.Frame(root, padding="10")
    header_frame.pack(fill=tk.X, pady=(10, 20))

    header_label = ttk.Label(header_frame, text="Lab Visage Entry Admin", font=TITLE_FONT)
    header_label.pack(pady=10)

    # Setting frame
    setting_frame = ttk.Frame(root, padding="10")
    setting_frame.pack(side=tk.LEFT, anchor='nw', padx=20, pady=10, fill=tk.BOTH, expand=True)

    setting_label = ttk.Label(setting_frame, text='Settings', font=TITLE_FONT)
    setting_label.pack(pady=10)

    button_width = 15  # Define button width for consistency

    db_status_label = ttk.Label(setting_frame, text="Database Status: Connecting....n", font=BUTTON_FONT)
    db_status_label.pack(pady=10)

    data_entry_btn = ttk.Button(setting_frame, text='Insert User Data', command=lambda: DataEntryForm(root),
                                style='TButton', width=button_width)
    data_entry_btn.pack(pady=10)

    system_log_btn = ttk.Button(setting_frame, text='System Logs', command=TkinterDisplayLog.choose_log_file,
                                style='TButton', width=button_width)
    system_log_btn.pack(pady=10)

    update_face_btn = ttk.Button(setting_frame, text='Train Face', command=train_model.create_gui,
                                 style='TButton', width=button_width)
    update_face_btn.pack(pady=10)

    device_status_btn = ttk.Button(setting_frame, text='Device Status', command=DeviceStatus.create_gui,
                                   style='TButton', width=button_width)
    device_status_btn.pack(pady=10)

    list_names_btn = ttk.Button(setting_frame, text='List Names', command=showlect.create_gui, style='TButton',
                                width=button_width)
    list_names_btn.pack(pady=10)

    # Add the text box
    lorem_text = (
        "\t\t\tWELCOME TO LAB VISAGE ENTRY ADMIN\b\n\n"
        "\nInsert User Data is used to enroll the new user to the face recognition system. "
        "It will ask user to enter their Name, IC Number and Telephone Number\n\n"
        
        "System Log is for checking the admin logs such when the last training executed, errors in the system and more"
        "Face Req is for whose unlocked the door, face recognition error\n\n"
        
        "Train face feature will train the face that captured to a encoding file "
        "then this file will upload to raspberry pi for face recognition. "
        "It will take several times to finish all the face that will be trained. "
        "**Notes** Use these feature everytime a new user added\n\n"
        
        "Device Status feature will give the CPU and RAM usage to the admin and "
        "check if the raspberry pi is connected.\n\n"
        
        "List Names is used to list all the names that given access to the door. "
        "There is other feature such as Delete and Update the user information\n\n"
        "Thank you for using LVE ADMIN"
    )

    text_box_frame = ttk.Frame(root, padding="10")
    text_box_frame.pack(side=tk.RIGHT, anchor='ne', padx=20, pady=10, fill=tk.BOTH, expand=True)

    text_box = tk.Text(text_box_frame, wrap=tk.WORD, background=button_color, foreground=foreground_color)
    text_box.insert(tk.END, lorem_text)
    text_box.config(state=tk.DISABLED)  # Make the text box read-only
    text_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)



    update_connection_status_in_thread(db_status_label)  # Start checking the database connection status

    root.mainloop()

if __name__ == '__main__':
    main()

