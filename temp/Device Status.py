import tkinter as tk
from tkinter import ttk
import psutil
import platform
from datetime import datetime

# Function to get system information for a specific host
def get_remote_system_info(host):
    try:
        uname = platform.uname()
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp)

        return {
            "System": uname.system,
            "Node Name": uname.node,
            "Release": uname.release,
            "Version": uname.version,
            "Machine": uname.machine,
            "Processor": uname.processor,
            "Boot Time": bt.strftime("%Y-%m-%d %H:%M:%S"),
            "CPU Count": psutil.cpu_count(logical=True),
            "Total Memory": f"{psutil.virtual_memory().total / (1024 ** 3):.2f} GB",
            "Available Memory": f"{psutil.virtual_memory().available / (1024 ** 3):.2f} GB",
            "Used Memory": f"{psutil.virtual_memory().used / (1024 ** 3):.2f} GB",
            "Memory Usage": f"{psutil.virtual_memory().percent}%",
        }
    except Exception as e:
        return {"Error": str(e)}

# Function to display system information for local and remote devices
def display_system_info():
    app = tk.Tk()
    app.title("Server Status and System Information")


    # Get remote system information (replace "remote_host" with actual remote host)
    remote_info = get_remote_system_info("192.168.0.254")

    remote_info_text = "\n".join([f"{key}: {value}" for key, value in remote_info.items()])

    remote_system_info_label = ttk.Label(app, text="Remote System Information:", font=("Helvetica", 12), justify="left")
    remote_system_info_label.pack(pady=10)

    remote_system_info_label = ttk.Label(app, text=remote_info_text, font=("Helvetica", 10), justify="left", wraplength=500)
    remote_system_info_label.pack(pady=5)

    app.mainloop()

display_system_info()
