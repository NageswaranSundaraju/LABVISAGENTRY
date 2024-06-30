import tkinter as tk
from tkinter import messagebox
import mysql.connector
import DeviceStatus
from CaptureFace import capture_images
import TkinterDisplayLog
import train_model
import showlect
import logging
import scp



class LVEAdminApp:

    def __init__(self, root):

        self.root = root
        self.root.title("LVE ADMIN")
        self.root.geometry("850x500")

        # Fonts
        self.TITLE_FONT = ("Arial", 40, "bold")
        self.NORMAL_FONT = ("Arial", 15)
        self.BUTTON_FONT = ("Arial", 12)

        # Button size
        self.BUTTON_WIDTH = 20
        self.BUTTON_HEIGHT = 2

        self.create_widgets()

        self.check_db_connection()  # Check DB connection initially
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        file_handler = logging.FileHandler('app.log')
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)


    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, width=955, height=100)
        header_frame.pack(pady=(10, 20))

        header_label = tk.Label(header_frame, text="Lab Visage Entry Admin", font=self.TITLE_FONT)
        header_label.pack(pady=10)

        # Detail Section
        detail_frame = tk.Frame(self.root, width=400, height=300)
        detail_frame.pack(side=tk.LEFT, anchor='nw', padx=20, pady=10)

        name_label = tk.Label(detail_frame, text='NAME', font=self.NORMAL_FONT)
        name_label.grid(row=0, column=0, pady=10, padx=10, sticky='w')
        noic_label = tk.Label(detail_frame, text='NO IC', font=self.NORMAL_FONT)
        noic_label.grid(row=1, column=0, pady=10, padx=10, sticky='w')
        notel_label = tk.Label(detail_frame, text='NO TEL', font=self.NORMAL_FONT)
        notel_label.grid(row=2, column=0, pady=10, padx=10, sticky='w')

        self.name_entry = tk.Entry(detail_frame, font=self.NORMAL_FONT)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)
        self.noic_entry = tk.Entry(detail_frame, font=self.NORMAL_FONT)
        self.noic_entry.grid(row=1, column=1, padx=10, pady=10)
        self.notel_entry = tk.Entry(detail_frame, font=self.NORMAL_FONT)
        self.notel_entry.grid(row=2, column=1, padx=10, pady=10)

        open_cam_btn = tk.Button(detail_frame, text='OPEN CAMERA', command=self.open_camera, font=self.BUTTON_FONT,
                                 width=self.BUTTON_WIDTH, height=self.BUTTON_HEIGHT)
        open_cam_btn.grid(row=4, column=1, pady=20, columnspan=2, padx=10)

        enroll_btn = tk.Button(detail_frame, text='Enroll Face', command=self.enroll_face, font=self.BUTTON_FONT,
                               width=self.BUTTON_WIDTH, height=self.BUTTON_HEIGHT)
        enroll_btn.grid(row=1, column=2, padx=30, pady=10, ipadx=10)

        clear_btn = tk.Button(detail_frame, text='Clear', command=self.clear_entries, font=self.BUTTON_FONT,
                              width=self.BUTTON_WIDTH, height=self.BUTTON_HEIGHT)
        clear_btn.grid(row=2, column=2, padx=30, pady=10, ipadx=20)

        # Setting frame
        self.setting_frame = tk.Frame(self.root, width=200, height=300)
        self.setting_frame.pack(side=tk.LEFT, anchor='nw', padx=20, pady=10)

        setting_label = tk.Label(self.setting_frame, text='Settings', font=self.TITLE_FONT)
        setting_label.pack(pady=10)



        system_log_btn = tk.Button(self.setting_frame, text='System Logs', command=TkinterDisplayLog.choose_log_file,
                                   font=self.BUTTON_FONT, width=self.BUTTON_WIDTH, height=self.BUTTON_HEIGHT)
        system_log_btn.pack(pady=10, ipadx=10)

        update_face_btn = tk.Button(self.setting_frame, text='Refresh', command=train_model.create_gui,
                                    font=self.BUTTON_FONT, width=self.BUTTON_WIDTH, height=self.BUTTON_HEIGHT)
        update_face_btn.pack(pady=10, ipadx=10)

        device_status_btn = tk.Button(self.setting_frame, text='Device Status', command=DeviceStatus.create_gui,
                                      font=self.BUTTON_FONT, width=self.BUTTON_WIDTH, height=self.BUTTON_HEIGHT)
        device_status_btn.pack(pady=10, ipadx=10)

        list_names_btn = tk.Button(self.setting_frame, text='List Names', command=showlect.create_gui,
                                   font=self.BUTTON_FONT, width=self.BUTTON_WIDTH, height=self.BUTTON_HEIGHT)
        list_names_btn.pack(pady=10, ipadx=10)

        self.db_status_label = tk.Label(self.setting_frame, text='Database: Disconnected', font=self.NORMAL_FONT,
                                        fg='red')
        self.db_status_label.pack(pady=10)

    def check_db_connection(self):
        try:
            connection = mysql.connector.connect(
                user='NAGES',
                password='ROOT',
                host='192.168.0.254',
                database='lvedb'
            )
            if connection.is_connected():
                self.db_status_label.config(text='Database: Connected', fg='green')
                connection.close()
            else:
                self.db_status_label.config(text='Database: Disconnected', fg='red')
        except mysql.connector.Error as err:
            self.db_status_label.config(text='Database: Disconnected', fg='red')
            logging.error(f"DATABASE ERROR {err}")

    def open_camera(self):
        username = self.noic_entry.get()
        if username.strip():
            capture_images(username)
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
                        user='NAGES',
                        password='ROOT',
                        host='192.168.0.254',
                        database='lvedb'
                    )
                    cursor = connection.cursor()
                    insert_query = "INSERT INTO lect (noic, name, notel) VALUES (%s, %s, %s)"
                    cursor.execute(insert_query, (noic, name, notel))
                    connection.commit()
                    cursor.close()
                    connection.close()
                    messagebox.showinfo("Success", "Data inserted successfully!")
                    self.logger.info(f"Data Added Name: {name} NoIC: {noic}")
                    self.clear_entries()
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Error: {err}")
                    logging.error(f"DATABASE ERROR {err}")
        else:
            messagebox.showwarning("Warning", "Please fill in all fields.")


if __name__ == '__main__':
    root = tk.Tk()
    app = LVEAdminApp(root)
    root.mainloop()
