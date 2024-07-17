import tkinter as tk
from tkinter import messagebox

# Predefined PIN for validation
CORRECT_PIN = "1234"
ATTEMPT_LIMIT = 5

def setup_pin_entry_window():
    """Sets up the PIN entry window"""
    global attempt_count
    attempt_count = 0

    def add_digit(digit):
        current_pin = pin_var.get()
        pin_var.set(current_pin + digit)

    def clear_pin():
        pin_var.set("")

    def validate_pin():
        global attempt_count
        entered_pin = pin_var.get()
        if entered_pin == CORRECT_PIN:
            messagebox.showinfo("Success", "PIN is correct!")
            root.destroy()
        else:
            attempt_count += 1
            if attempt_count >= ATTEMPT_LIMIT:
                error_box = messagebox.showerror("Access Denied", "Access Denied, Contact PIC")
                root.wait_window(error_box)  # Wait until the error box is closed
                root.destroy()  # Close the main window after the error box is closed
            else:
                messagebox.showerror("Error", "Incorrect PIN")
                clear_pin()

    root = tk.Tk()
    root.title("PIN Entry")
    pin_var = tk.StringVar()

    label = tk.Label(root, text="Enter your PIN:")
    label.grid(row=0, column=0, columnspan=3)

    pin_entry = tk.Entry(root, textvariable=pin_var)
    pin_entry.grid(row=1, column=0, columnspan=3)

    buttons = [
        ('1', 1, 0), ('2', 1, 1), ('3', 1, 2),
        ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
        ('7', 3, 0), ('8', 3, 1), ('9', 3, 2),
        ('0', 4, 1)
    ]
    keyFrame = tk.Frame(root)
    keyFrame.grid(row=2, column=0, columnspan=3)
    for (text, row, col) in buttons:
        button = tk.Button(keyFrame, text=text, command=lambda t=text: add_digit(t), width=10, height=3)
        button.grid(row=row, column=col, padx=5, pady=5)

    clear_button = tk.Button(keyFrame, text="Clear", command=clear_pin, width=10, height=3)
    clear_button.grid(row=4, column=0, padx=5, pady=5)

    submit_button = tk.Button(keyFrame, text="Submit", command=validate_pin, width=10, height=3)
    submit_button.grid(row=4, column=2, padx=5, pady=5)

    root.mainloop()


