import tkinter as tk
from tkinter import *
import DeviceStatus
#import train_model
from CaptureFace import capture_images  # Import the capture_images function

def main():
    global root
    root = tk.Tk()
    root.title("LVE ADMIN")
    root.geometry("955x500")

    HeaderTitle = tk.Label(root, text='Lab Visage Entry Admin', font=("Arial", 40, "bold"))
    HeaderTitle.pack(pady=10)

    # TextConfig
    NORMALTXT = ("Arial", 15)
    TITLETXT = ("Arial", 15, 'bold')

    # Detail Section
    Dframe = tk.Frame(root, height=250, width=250)
    Dframe.pack(side=LEFT, anchor='w', padx=40, ipadx=15)

    NameLabel = tk.Label(Dframe, text='NAME', font=(NORMALTXT))
    NameLabel.grid(row=0, column=0, pady=10)
    NOICLabel = tk.Label(Dframe, text='NO IC', font=(NORMALTXT))
    NOICLabel.grid(row=1, column=0, pady=10)
    NOTELLabel = tk.Label(Dframe, text='NO TEL', font=(NORMALTXT))
    NOTELLabel.grid(row=2, column=0, pady=10)

    global NameEntry, NOICEntry, NOTELEntry  # Declare as global variables to access them in other functions
    NameEntry = tk.Entry(Dframe,)
    NameEntry.grid(row=0, column=1)
    NameEntry.config(bg='White', fg='Black')
    NOICEntry = tk.Entry(Dframe,)
    NOICEntry.grid(row=1, column=1)
    NOICEntry.config(bg='White', fg='Black')
    NOTELEntry = tk.Entry(Dframe,)
    NOTELEntry.grid(row=2, column=1)
    NOTELEntry.config(bg='White', fg='Black')

    def open_camera():
        username = NameEntry.get()
        if username.strip():  # Check if the username is not empty
            capture_images(username)
        else:
            tk.messagebox.showwarning("Warning", "Please enter a name before opening the camera.")

    def clear_entries():
        NameEntry.delete(0, END)
        NOICEntry.delete(0, END)
        NOTELEntry.delete(0, END)

    OPENCAMBtn = tk.Button(Dframe, text='OPEN CAMERA', command=open_camera)  # Link the button to the open_camera function
    OPENCAMBtn.grid(row=3, column=1, pady=20, columnspan=1)

    EnrollBtn = tk.Button(Dframe, text='Enroll Face')
    EnrollBtn.grid(row=1, column=2, padx=50, ipadx=5)

    ClearBtn = tk.Button(Dframe, text='Clear', command=clear_entries)
    ClearBtn.grid(row=2, column=2, padx=50, ipadx=25)

    # Setting frame
    settingFrame = tk.Frame(root, bg='dark grey', height=150, width=250)
    settingFrame.pack(side=LEFT, anchor='w', padx=50, ipady=40, ipadx=80)

    settinglabel = tk.Label(settingFrame, text='Setting', font=TITLETXT)
    settinglabel.pack(anchor='w', pady=5, padx=5)

    SystemLogBtn = tk.Button(settingFrame, text='System Logs', activebackground='dark grey')
    SystemLogBtn.pack(ipady=10, pady=10)
    UpdateFaceBtn = tk.Button(settingFrame, text='Refresh', activebackground='dark grey')
    UpdateFaceBtn.pack(ipady=10, pady=10)
    StatusBtn = tk.Button(settingFrame, text='Device Status', activebackground='dark grey', command=DeviceStatus.create_gui)
    StatusBtn.pack(ipady=10, pady=10)

    # Run the Tkinter event loop
    root.mainloop()

if __name__ == '__main__':
    main()
