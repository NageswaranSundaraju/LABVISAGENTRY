import tkinter as tk
import paramiko

def get_remote_system_info():
    hostname = '192.168.0.12'
    username = 'root'
    password = 'Admin'

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
        return f"Error: {e}"

def fetch_system_info():

    system_info = get_remote_system_info()
    device_name, ram_info, cpu_info = system_info

    ram_usage = ram_info.split()[2]
    cpu_usage = cpu_info.split(',')[0].split()[1]

    hostname.config(text=device_name)
    cpu.config(text=cpu_usage)
    ram.config(text=ram_usage)

def create_gui():
    root = tk.Tk()
    root.title("Remote System Information")

    # Create button to fetch system information
    fetch_button = tk.Button(root, text="Fetch System Info", command=fetch_system_info, font=("Arial", 14))
    fetch_button.pack(pady=10)

    # Create label to display system information

    global info_label, hostname, ram,cpu

    # info_label = tk.Label(root, text="", wraplength=500, font=("Arial", 12), padx=20, pady=20, justify=tk.LEFT)
    # info_label.pack()

    hostname = tk.Label(root, text='')
    hostname.pack()
    cpu = tk.Label(root, text='')
    cpu.pack()
    ram = tk.Label(root, text='')
    ram.pack()



    root.mainloop()

# Call the function to create the GUI



