import tkinter as tk
from tkinter import ttk
import paramiko
import threading

def get_remote_system_info():
    hostname = '192.168.1.100'
    username = 'pi'
    password = 'admin'

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
        return f"Error: {e}", "", ""

def fetch_system_info():
    def task():
        system_info = get_remote_system_info()
        device_name, ram_info, cpu_info = system_info

        if "Error:" in device_name:
            info_label.config(text="Not connected")
            hostname_label.config(text="")
            ram_label.config(text="")
            cpu_label.config(text="")
        else:
            ram_usage = ram_info.split()[2]
            cpu_usage = cpu_info.split(',')[0].split()[1]

            info_label.config(text="")
            hostname_label.config(text=f"Hostname: {device_name}")
            ram_label.config(text=f"RAM Usage: {ram_usage} MB")
            cpu_label.config(text=f"CPU Usage: {cpu_usage} %")

        progress_bar.stop()
        fetch_button.config(state=tk.NORMAL)

    fetch_button.config(state=tk.DISABLED)
    info_label.config(text="Connecting...")
    progress_bar.start()
    threading.Thread(target=task).start()

def create_gui():
    root = tk.Tk()
    root.title("Remote System Information")

    global info_label, hostname_label, ram_label, cpu_label, progress_bar, fetch_button

    # Create button to fetch system information
    fetch_button = tk.Button(root, text="Fetch System Info", command=fetch_system_info, font=("Arial", 14))
    fetch_button.pack(pady=10)

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

