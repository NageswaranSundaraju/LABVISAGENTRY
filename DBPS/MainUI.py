import tkinter as tk
from tkinter import messagebox
import mysql.connector
import DeviceStatus
from CaptureFace import capture_images
import TkinterDisplayLog
import train_model
import showlect
import logging

logging.basicConfig(filename='admin.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():

    root = tk.Tk()
    root.title("LVE ADMIN")
    root.geometry("750x450")

    # Fonts
    TITLE_FONT = ("Arial", 40, "bold")
    NORMAL_FONT = ("Arial", 15)
    BUTTON_FONT = ("Arial", 12)

    # Header
    header_frame = tk.Frame(root, bg="lightgrey", width=955, height=100)
    header_frame.pack(pady=(10, 20))

    header_label = tk.Label(header_frame, text="Lab Visage Entry Admin", font=TITLE_FONT)
    header_label.pack(pady=10)

    # Detail Section
    detail_frame = tk.Frame(root, width=400, height=300)
    detail_frame.pack(side=tk.LEFT, anchor='nw', padx=20, pady=10)

    name_label = tk.Label(detail_frame, text='NAME', font=NORMAL_FONT)
    name_label.grid(row=0, column=0, pady=10, padx=10, sticky='w')
    noic_label = tk.Label(detail_frame, text='NO IC', font=NORMAL_FONT)
    noic_label.grid(row=1, column=0, pady=10, padx=10, sticky='w')
    notel_label = tk.Label(detail_frame, text='NO TEL', font=NORMAL_FONT)
    notel_label.grid(row=2, column=0, pady=10, padx=10, sticky='w')

    name_entry = tk.Entry(detail_frame, font=NORMAL_FONT)
    name_entry.grid(row=0, column=1, padx=10, pady=10)
    noic_entry = tk.Entry(detail_frame, font=NORMAL_FONT)
    noic_entry.grid(row=1, column=1, padx=10, pady=10)
    notel_entry = tk.Entry(detail_frame, font=NORMAL_FONT)
    notel_entry.grid(row=2, column=1, padx=10, pady=10)

    def open_camera():
        username = noic_entry.get()
        if username.strip():
            capture_images(username)
        else:
            messagebox.showwarning("Warning", "Please enter a name before opening the camera.")

    def clear_entries():
        name_entry.delete(0, tk.END)
        noic_entry.delete(0, tk.END)
        notel_entry.delete(0, tk.END)

    def enroll_face():
        name = name_entry.get()
        noic = noic_entry.get()
        notel = notel_entry.get()

        if name.strip() and noic.strip() and notel.strip():
            summary = f"Name: {name}\nNo IC: {noic}\nNo Tel: {notel}\n"
            confirm = messagebox.askokcancel("Confirm Data",
                                             f"Please confirm the following data will be added to the database:\n\n"
                                             f"{summary}")
            if confirm:
                try:
                    connection = mysql.connector.connect(
                        user='Nages',
                        password='admin',
                        host='192.168.146.1',
                        database='lvedb'
                    )
                    cursor = connection.cursor()
                    insert_query = "INSERT INTO lect (noic, name, notel) VALUES (%s, %s, %s)"
                    cursor.execute(insert_query, (noic, name, notel))
                    connection.commit()
                    cursor.close()
                    connection.close()
                    messagebox.showinfo("Success", "Data inserted successfully!")
                    logging.info(f"Data Added Name: {name} NoIC: {noic}")
                    clear_entries()
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Error: {err}")
                    logging.error(f"DATABASE ERROR {err}")
        else:
            messagebox.showwarning("Warning", "Please fill in all fields.")

    open_cam_btn = tk.Button(detail_frame, text='OPEN CAMERA', command=open_camera, font=BUTTON_FONT)
    open_cam_btn.grid(row=4, column=1, pady=20, columnspan=2, padx=10)

    enroll_btn = tk.Button(detail_frame, text='Enroll Face', command=enroll_face, font=BUTTON_FONT)
    enroll_btn.grid(row=1, column=2, padx=30, pady=10, ipadx=10)

    clear_btn = tk.Button(detail_frame, text='Clear', command=clear_entries, font=BUTTON_FONT)
    clear_btn.grid(row=2, column=2, padx=30, pady=10, ipadx=20)

    # Setting frame
    setting_frame = tk.Frame(root, bg='lightgrey', width=200, height=300)
    setting_frame.pack(side=tk.LEFT, anchor='nw', padx=20, pady=10)

    setting_label = tk.Label(setting_frame, text='Settings', font=TITLE_FONT)
    setting_label.pack(pady=10)

    system_log_btn = tk.Button(setting_frame, text='System Logs', command=TkinterDisplayLog.choose_log_file,
                               font=BUTTON_FONT)
    system_log_btn.pack(pady=10, ipadx=10)

    update_face_btn = tk.Button(setting_frame, text='Refresh', command=train_model.create_gui,
                                font=BUTTON_FONT)
    update_face_btn.pack(pady=10, ipadx=10)

    device_status_btn = tk.Button(setting_frame, text='Device Status', command=DeviceStatus.create_gui,
                                  font=BUTTON_FONT)
    device_status_btn.pack(pady=10, ipadx=10)

    list_names_btn = tk.Button(setting_frame, text='List Names', command=showlect.create_gui, font=BUTTON_FONT)
    list_names_btn.pack(pady=10, ipadx=10)

    root.mainloop()


if __name__ == '__main__':
    main()


