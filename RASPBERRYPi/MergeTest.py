import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import face_recognition
import imutils
from imutils.video import VideoStream, FPS
import pickle
import time
import mysql.connector
from mysql.connector import Error
import datetime
import logging
import serial

from PinMode import setup_pin_entry_window

logging.basicConfig(filename='../DBPS/facereq.log', level=logging.INFO, format='%(asctime)s - %(message)s')


class FaceRecognitionApp:
    def __init__(self, root):


        self.root = root
        self.root.title("LAB VISAGE ENTRY")
        self.root.geometry('955x500')
        self.root.resizable(0, 0)

        self.current_name = "unknown"
        self.encodings_file = "../DBPS/encodings.pickle"
        self.data = pickle.loads(open(self.encodings_file, "rb").read())
        self.ser = serial.Serial('/dev/ttyUSB0', 9600)
        # Use DirectShow backend on Windows
        self.cap = VideoStream(src=0, framerate=30).start()
        time.sleep(2.0)
        self.fps = FPS().start()

        self.build_gui()
        self.update_frame()

    def build_gui(self):
        NORMALTXT = ("Arial")

        HeaderTitle = tk.Label(self.root, text='Welcome To Lab Visage Entry', font=("Arial", 40, "bold"))
        MainFrame = tk.Frame(self.root)
        Cam = tk.Frame(MainFrame, bg="black", height=350, width=450)
        DetailFrame = tk.Frame(MainFrame, height=310, width=430)

        ScanBtn = tk.Button(DetailFrame, text='SCAN FACE', bg='Green', activebackground='Green', height=5, width=15,
                            command=self.restart_program)
        NameLabel = tk.Label(DetailFrame, text='NAMA', font=(NORMALTXT))
        NoICLabel = tk.Label(DetailFrame, text='NO IC', font=(NORMALTXT))
        self.NameEntry = tk.Label(DetailFrame, text="", bg='White', fg='Black')
        self.NoICEntry = tk.Label(DetailFrame, text='', bg='White', fg='Black')
        self.dbcon = tk.Label(self.root, text='', fg='White')

        HeaderTitle.pack()
        MainFrame.pack(expand=True, pady=20, padx=20, fill='both')
        Cam.grid(row=1, column=0, padx=20, pady=20)
        ScanBtn.grid(row=5, columnspan=3, pady=40)
        DetailFrame.grid(row=1, column=1, padx=50, pady=20)
        NameLabel.grid(row=0, column=0, pady=30)
        NoICLabel.grid(row=1, column=0)
        self.NameEntry.grid(row=0, column=1)
        self.NoICEntry.grid(row=1, column=1)
        self.dbcon.pack()

        self.camera_label = tk.Label(Cam, height=350, width=450)
        self.camera_label.pack()

    def process_frame(self, frame):
        frame = imutils.resize(frame, width=500)
        boxes = face_recognition.face_locations(frame)
        encodings = face_recognition.face_encodings(frame, boxes)
        names = []

        face_detected = False  # Add a flag to check if a face is detected

        for encoding in encodings:
            matches = face_recognition.compare_faces(self.data["encodings"], encoding)
            name = "Unknown"
            if True in matches:
                face_detected = True  # Set the flag to True if a face is matched
                matched_idxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                for i in matched_idxs:
                    name = self.data["names"][i]
                    counts[name] = counts.get(name, 0) + 1
                name = max(counts, key=counts.get)
                if self.current_name != name:
                    self.current_name = name
                    print(self.current_name)
                    self.fetch_user_info(self.current_name)
                    self.ser.write(b'1')
                    logging.info(f"Access granted for {self.current_name}")
            names.append(name)


        if not face_detected:  # Show message if no face is detected
            self.current_name = "Unknown"
            self.NameEntry.config(text="Access Denied")
            self.NoICEntry.config(text="")
            return frame

        for ((top, right, bottom, left), name) in zip(boxes, names):
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 225), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, .8, (0, 255, 255), 2)
        return frame

    def fetch_user_info(self, noic):
        try:
            connection = mysql.connector.connect(
                user='Nages',
                password='admin',
                host='192.168.146.1',
                database='lvedb'
            )
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("SELECT name, noic FROM lect WHERE noic = %s", (noic,))
                record = cursor.fetchone()
                if record:
                    self.NameEntry.config(text=record[0])
                    self.NoICEntry.config(text=record[1])
                    messagebox.showinfo("Access Granted", f"Welcome {record[0]}")

                    # Logging access
                    access_log_message = f"Access granted to {record[0]} at {datetime.datetime.now()}"
                    logging.info(access_log_message)
                    self.ser.write(b'1')

                else:
                    self.NameEntry.config(text="Not found")
                    self.NoICEntry.config(text="Not found")
        except Error as e:
            messagebox.showerror("Database Error", f"Error connecting to MySQL: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()



    def update_frame(self):
        if not self.cap.stream.isOpened():
            return

        frame = self.cap.read()
        frame = self.process_frame(frame)

        # Convert the image from OpenCV format to PIL format
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)

        # Update the GUI window with the new image
        self.camera_label.config(image=image)
        self.camera_label.image = image

        # Repeat after 10 milliseconds
        self.camera_label.after(10, self.update_frame)

    def restart_program(self):
        self.cap.stop()
        self.fps.stop()
        self.root.after(500, self.reinitialize)

    def reinitialize(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.__init__(self.root)


if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()

