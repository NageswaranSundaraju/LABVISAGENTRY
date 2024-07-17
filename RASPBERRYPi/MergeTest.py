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
import PinMode
import json
import qrcode

logging.basicConfig(filename='../DBPS/facereq.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Load the JSON configuration file
with open('config.json') as config_file:
    config = json.load(config_file)
class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LAB VISAGE ENTRY")
        self.root.geometry('955x500')
        self.root.resizable(0, 0)

        self.current_name = "unknown"
        self.encodings_file = "../DBPS/encodings.pickle"
        self.data = pickle.loads(open(self.encodings_file, "rb").read())
        self.cap = VideoStream(src=0, framerate=30).start()
        self.fps = FPS().start()

        self.failed_attempts = 0
        self.face_detected = False
        self.face_detected_time = None

        self.build_gui()
        self.update_frame()

    def build_gui(self):
        NORMALTXT = ("Arial")

        HeaderTitle = tk.Label(self.root, text='Welcome To Lab Visage Entry', font=("Arial", 40, "bold"))
        MainFrame = tk.Frame(self.root)
        Cam = tk.Frame(MainFrame, bg="black", height=350, width=450)
        DetailFrame = tk.Frame(MainFrame, height=310, width=430)

        ScanBtn = tk.Button(DetailFrame, text='SCAN FACE', bg='Green', activebackground='Green', height=5, width=15, command=self.restart_application)
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

        self.instruction_label = tk.Label(DetailFrame, text="Show your face to the camera and hold still", font=("Arial", 14))
        self.instruction_label.grid(row=6, columnspan=3, pady=10)

    def restart_application(self):
        self.root.destroy()
        root = tk.Tk()
        app = FaceRecognitionApp(root)
        root.mainloop()

    def process_frame(self, frame):
        frame = imutils.resize(frame, width=500)
        boxes = face_recognition.face_locations(frame)
        encodings = face_recognition.face_encodings(frame, boxes)
        names = []

        if len(boxes) > 0 and not self.face_detected:
            self.face_detected = True
            self.face_detected_time = time.time()
            self.instruction_label.config(text="Hold your face still")

        if self.face_detected and (time.time() - self.face_detected_time) < 1:
            return frame

        self.face_detected = False  # Reset the flag after processing the face
        self.instruction_label.config(text="Show your face to the camera and hold still")

        for encoding in encodings:
            matches = face_recognition.compare_faces(self.data["encodings"], encoding, tolerance=0.4)
            name = "Unknown"
            if True in matches:
                matched_idxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                for i in matched_idxs:
                    name = self.data["names"][i]
                    counts[name] = counts.get(name, 0) + 1
                name = max(counts, key=counts.get)
                if self.current_name != name:
                    self.current_name = name
                    self.failed_attempts = 0
                    print(name)
                    self.fetch_user_info(self.current_name)
                    logging.info(f"Access granted for {self.current_name}")

            else:
                self.failed_attempts += 1
                print("Unknown")
                if self.failed_attempts >= 4:
                    print("Access Denied")
                    self.show_access_denied()

            names.append(name)

        for ((top, right, bottom, left), name) in zip(boxes, names):
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 255, 225), 1)
            # y = top - 15 if top - 15 > 15 else top + 15
            # cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, .4, (255, 255, 255), 1)
        return frame

    def fetch_user_info(self, noic):
        try:
            connection = mysql.connector.connect(
                user=config["database"]["user"],
                password=config["database"]["password"],
                host=config["database"]["host"],
                database=config["database"]["db"]
            )
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("SELECT name, noic FROM lect WHERE noic = %s", (noic,))
                record = cursor.fetchone()
                if record:
                    self.NameEntry.config(text=record[0])
                    self.NoICEntry.config(text=record[1])
                    messagebox.showinfo("Access Granted", f"Welcome {record[0]}")

                    logging.info(f"Access granted to {record[0]} at {datetime.datetime.now()}")
                else:
                    self.NameEntry.config(text="Not found")
                    self.NoICEntry.config(text="Not found")
        except Error as e:
            messagebox.showerror("Database Error", f"Error connecting to MySQL: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def show_qr_code(self):
        # Generate a QR code
        qr_data = "https://t.me/VisageEntryBot"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')

        # Display the QR code in a new window
        qr_window = tk.Toplevel(self.root)
        qr_window.title("Access Denied - QR Code")

        img = ImageTk.PhotoImage(img)
        qr_label = tk.Label(qr_window, image=img)
        qr_label.image = img
        qr_label.pack(pady=20, padx=20)

        exit_button = tk.Button(qr_window, text="Exit", command=qr_window.destroy)
        exit_button.pack(pady=10)



        qr_window.mainloop()

    def show_access_denied(self):
        messagebox.showerror("Access Denied", "Access Denied. Please try again.")
        logging.info(f"Access denied after 4 failed attempts at {datetime.datetime.now()}")
        self.show_qr_code()



    def update_frame(self):
        if not self.cap.stream.isOpened():
            return

        frame = self.cap.read()
        frame = self.process_frame(frame)

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)

        self.camera_label.config(image=image)
        self.camera_label.image = image

        self.camera_label.after(10, self.update_frame)

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()
