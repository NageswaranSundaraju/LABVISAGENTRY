import tkinter as tk
from tkinter import messagebox
import sys
import os

def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

root = tk.Tk()
root.title("Restart Program Example")

restart_button = tk.Button(root, text="Restart", command=restart_program)
restart_button.pack(pady=20)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
