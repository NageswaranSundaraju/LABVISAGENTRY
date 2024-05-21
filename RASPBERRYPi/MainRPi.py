import tkinter as tk
import cv2
from mysql.connector import Error
from PIL import Image, ImageTk
from DBConn import condb, dbstat


def ShowData():
    no_ic_input = input('Enter IC')
    cnx = condb()
    if cnx:
        name, no_ic = "No Data", "No Data"
        try:

            cursor = cnx.cursor()
            query = "SELECT first_name,no_ic FROM employees WHERE no_ic = %s;"
            cursor.execute(query, (no_ic_input,))
            row = cursor.fetchone()
            if row:
                name, no_ic = row
            else:
                pass
        except Error as err:
            print(err)
        finally:
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()
                print('db closed')
    NameEntry.config(text=name)
    NoICEntry.config(text=no_ic)

def update_frame():
    ret, frame = cap.read()
    if ret:
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        camera_label.imgtk = imgtk
        camera_label.configure(image=imgtk)
    camera_label.after(5, update_frame)

def Interface():
    global NameEntry, NoICEntry, camera_label, cap, dbcon

    root = tk.Tk()
    root.title("LAB VISAGE ENTRY")
    root.geometry('955x500')
    root.resizable(0, 0)

    NORMALTXT = ("Arial")

    HeaderTitle = tk.Label(root, text='Welcome To Lab Visage Entry', font=("Arial", 40, "bold"))
    MainFrame = tk.Frame(root)
    Cam = tk.Frame(MainFrame, bg="black", height=350, width=450)
    DetailFrame = tk.Frame(MainFrame, height=310, width=430)

    ScanBtn = tk.Button(DetailFrame, text='SCAN FACE', bg='Green', activebackground='Green', command=ShowData, height=5, width=15)
    NameLabel = tk.Label(DetailFrame, text='NAMA', font=(NORMALTXT))
    NoICLabel = tk.Label(DetailFrame, text='NO IC', font=(NORMALTXT))
    NameEntry = tk.Label(DetailFrame, text="", bg='White', fg='Black')
    NoICEntry = tk.Label(DetailFrame, text='', bg='White', fg='Black')
    dbcon = tk.Label(root, text='', fg='White')

    HeaderTitle.pack()
    MainFrame.pack(expand=True, pady=20, padx=20, fill='both')
    Cam.grid(row=1, column=0, padx=20, pady=20)
    ScanBtn.grid(row=5, columnspan=3, pady=40)
    DetailFrame.grid(row=1, column=1, padx=50, pady=20)
    NameLabel.grid(row=0, column=0, pady=30)
    NoICLabel.grid(row=1, column=0)
    NameEntry.grid(row=0, column=1)
    NoICEntry.grid(row=1, column=1)
    dbcon.pack()

    camera_label = tk.Label(Cam, height=350, width=450)
    camera_label.pack()

    cap = cv2.VideoCapture(0)
    update_frame()

    # Update dbcon label with the current database connection status
    if dbstat == 'DB is Connected':
        dbcon.config(text=dbstat, fg='Green')
    else:
        dbcon.config(text=dbstat, fg ='Red')

    root.mainloop()
    cap.release()


Interface()
