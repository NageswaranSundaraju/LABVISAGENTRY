import tkinter as tk
from tkinter import messagebox

# Function to show "Unlocked" message
def show_unlocked():
    messagebox.showinfo("Status", "Unlocked")

# Function to show "Not Recognized" message
def show_not_recognized():
    messagebox.showwarning("Status", "Not Recognized")


