import tkinter as tk
from tkinter import ttk, messagebox
import paramiko
import threading
import json
import logging

logging.basicConfig(filename="admin.log", level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_remote_system_info(hostname, username, password):
    try:
        # Establish SSH connection
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname, username=username, password=password)

        # Execute commands to get RAM and CPU usage
        stdin, stdout, stderr = ssh_client.exec_command('hostname')
        device_name = stdout.read().decode().strip()

        stdin, stdout, stderr = ssh_client.exec_command('free -m | grep Mem')
        ram_info = stdout.read().decode().strip()

        stdin, stdout, stderr = ssh_client.exec_command('top -bn1 | grep "Cpu(s)"')
        cpu_info = stdout.read().decode().strip()

        # Close the SSH connection
        ssh_client.close()

        return device_name, ram_info, cpu_info  # Return as a single tuple
    except Exception as e:
        logging.error(f"Error: {e}")
        return f"Error: {e}", "", ""

def fetch_system_info(device_index):
    def task():
        with open('devices.json') as json_file:
            data = json.load(json_file)
            device = data['devices'][device_index]
            hostname = device['hostname']
            username = device['username']
            password = device['password']
            device_name = device['name']

        # Update connection info display
        connection_info.set(f"Connecting to {hostname} ({device_name})...")

        system_info = get_remote_system_info(hostname, username, password)
        device_name_ssh, ram_info, cpu_info = system_info

        if "Error:" in device_name_ssh:
            info_label.config(text="Not connected")
            hostname_label.config(text="")
            ram_label.config(text="")
            cpu_label.config(text="")
        else:
            ram_usage = ram_info.split()[2]
            cpu_usage = cpu_info.split(',')[0].split()[1]

            info_label.config(text="")
            hostname_label.config(text=f"Device: {device_name}")
            ram_label.config(text=f"RAM Usage: {ram_usage} MB")
            cpu_label.config(text=f"CPU Usage: {cpu_usage} %")

        progress_bar.stop()
        fetch_button.config(state=tk.NORMAL)
        connection_info.set("")  # Clear connection info after fetching

    fetch_button.config(state=tk.DISABLED)
    info_label.config(text="Connecting...")
    progress_bar.start()
    threading.Thread(target=task).start()

def add_device():
    def save_device():
        new_device = {
            "name": name_entry.get(),
            "hostname": hostname_entry.get(),
            "username": username_entry.get(),
            "password": password_entry.get()
        }

        try:
            with open('devices.json', 'r') as json_file:
                data = json.load(json_file)
                data['devices'].append(new_device)

            with open('devices.json', 'w') as json_file:
                json.dump(data, json_file, indent=4)

            messagebox.showinfo("Success", "Device added successfully!")
            add_device_window.destroy()

            # Update dropdown menu
            update_dropdown()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add device: {e}")

    add_device_window = tk.Toplevel()
    add_device_window.title("Add New Device")
    add_device_window.geometry("500x500")  # Set the size of the window

    tk.Label(add_device_window, text="Device Name:").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(add_device_window, text="Hostname/IP:").grid(row=1, column=0, padx=10, pady=5)
    tk.Label(add_device_window, text="Username:").grid(row=2, column=0, padx=10, pady=5)
    tk.Label(add_device_window, text="Password:").grid(row=3, column=0, padx=10, pady=5)

    name_entry = tk.Entry(add_device_window, width=30)
    name_entry.grid(row=0, column=1, padx=10, pady=5)
    hostname_entry = tk.Entry(add_device_window, width=30)
    hostname_entry.grid(row=1, column=1, padx=10, pady=5)
    username_entry = tk.Entry(add_device_window, width=30)
    username_entry.grid(row=2, column=1, padx=10, pady=5)
    password_entry = tk.Entry(add_device_window, width=30, show='*')
    password_entry.grid(row=3, column=1, padx=10, pady=5)

    save_button = tk.Button(add_device_window, text="Save Device", command=save_device)
    save_button.grid(row=4, column=0, columnspan=2, pady=10)

def update_dropdown():
    device_dropdown['values'] = []  # Clear current values

    # Load devices from JSON file
    with open('devices.json') as json_file:
        data = json.load(json_file)
        device_list = [device['name'] for device in data['devices']]

    device_var.set("")  # Clear selected value
    device_dropdown['values'] = device_list  # Update dropdown values

def create_gui():
    global info_label, hostname_label, ram_label, cpu_label, progress_bar, fetch_button, device_dropdown, device_var, connection_info

    root = tk.Tk()
    root.title("Remote System Information")

    # Load devices from JSON file initially
    with open('devices.json') as json_file:
        data = json.load(json_file)
        device_list = [device['name'] for device in data['devices']]

    device_var = tk.StringVar()
    device_dropdown = ttk.Combobox(root, textvariable=device_var, values=device_list)
    device_dropdown.pack(pady=10)

    fetch_button = tk.Button(root, text="Fetch System Info", command=lambda: fetch_system_info(device_dropdown.current()), font=("Arial", 14))
    fetch_button.pack(pady=10)

    add_button = tk.Button(root, text="Add Device", command=add_device)
    add_button.pack(pady=10)

    # Connection info label
    connection_info = tk.StringVar()
    connection_label = tk.Label(root, textvariable=connection_info, font=("Arial", 10), fg="blue")
    connection_label.pack(pady=5)

    # Create progress bar
    progress_bar = ttk.Progressbar(root, mode='indeterminate')
    progress_bar.pack(pady=10)

    # Create labels to display system information
    info_label = tk.Label(root, text="", wraplength=500, font=("Arial", 12), padx=20, pady=20, justify=tk.LEFT)
    info_label.pack()

    hostname_label = tk.Label(root, text="", font=("Arial", 12))
    hostname_label.pack()

    cpu_label = tk.Label(root, text="", font=("Arial", 12))
    cpu_label.pack()

    ram_label = tk.Label(root, text="", font=("Arial", 12))
    ram_label.pack()

    root.mainloop()

# Run the GUI
if __name__ == "__main__":
    create_gui()
