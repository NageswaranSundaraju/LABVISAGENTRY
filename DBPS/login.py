import tkinter as tk
from tkinter import messagebox
import json
import MainUI
import logging

# Configure logging
logging.basicConfig(filename="admin.log", level=logging.INFO, format="%(asctime)s - %(message)s")

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("300x200")  # Set initial size

        self.username_label = tk.Label(root, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.username_entry = tk.Entry(root)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        self.password_label = tk.Label(root, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="e")

        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.grid(row=2, columnspan=2, pady=10)

        # Load user data from JSON file
        with open("users.json", "r") as f:
            self.users_data = json.load(f)["users"]

        # Bind Enter key to log in function
        self.root.bind("<Return>", self.login_enter)

        # Make the grid layout responsive
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check credentials against loaded JSON data
        for user in self.users_data:
            if user["username"] == username and user["password"] == password:
                messagebox.showinfo("Login Successful", f"Welcome, {user['name']}!")
                logging.info(f"User '{user['name']}' logged in successfully.")
                self.root.destroy()
                MainUI.main()
                return

        # If no matching user found
        messagebox.showerror("Login Failed", "Incorrect username or password")

    def login_enter(self):
        self.login()


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
