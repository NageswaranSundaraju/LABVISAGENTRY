import tkinter as tk
import json
import base64
from cryptography.fernet import Fernet, InvalidToken

# File to store configurations
CONFIG_FILE = "database_config.json"
# Generate a key for encryption
KEY_FILE = "encryption_key.key"


# Function to generate or load encryption key
def load_or_generate_key():
    try:
        with open(KEY_FILE, "rb") as kf:
            key = kf.read()
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as kf:
            kf.write(key)
    return key


# Load or generate the key
encryption_key = load_or_generate_key()
cipher_suite = Fernet(encryption_key)


# Function to encrypt passwords
def encrypt_password(password):
    return cipher_suite.encrypt(password.encode())


# Function to decrypt passwords
def decrypt_password(encrypted_password):
    try:
        decrypted_password = cipher_suite.decrypt(encrypted_password)
        return decrypted_password.decode()
    except (ValueError, InvalidToken) as e:
        print(f"Error decrypting password: {e}")
        return None


# Function to save all configurations
def save_configs():
    try:
        encrypted_configs = []
        for config in configurations:
            encrypted_config = config.copy()  # Make a copy of the config dict
            encrypted_config["password"] = encrypt_password(config["password"]).decode(
                'utf-8')  # Convert bytes to base64 encoded string
            encrypted_configs.append(encrypted_config)

        with open(CONFIG_FILE, "w") as f:
            json.dump(encrypted_configs, f, indent=4)  # Pretty print JSON
        print("Configurations saved.")
    except Exception as e:
        print(f"Error saving configurations: {e}")


# Function to load all configurations
def load_configs():
    try:
        with open(CONFIG_FILE, "r") as f:
            encrypted_configs = json.load(f)
            decrypted_configs = []
            for encrypted_config in encrypted_configs:
                decrypted_config = encrypted_config.copy()
                encrypted_password = base64.b64decode(encrypted_config["password"])  # Decode base64 string to bytes
                decrypted_password = decrypt_password(encrypted_password)
                if decrypted_password is None:
                    # Handle decryption failure or invalid token
                    print(f"Failed to decrypt password for configuration: {encrypted_config['server_name']}")
                    continue
                decrypted_config["password"] = decrypted_password
                decrypted_configs.append(decrypted_config)

            configurations.clear()  # Clear current configurations
            configurations.extend(decrypted_configs)
            update_config_listbox()
        print("Configurations loaded.")
    except FileNotFoundError:
        print("No saved configurations found.")
    except Exception as e:
        print(f"Error loading configurations: {e}")


# Function to update the listbox with configuration names
def update_config_listbox():
    config_listbox.delete(0, tk.END)
    for config in configurations:
        config_listbox.insert(tk.END, config.get("server_name", ""))


# Function to load selected configuration into the GUI
def load_selected_config():
    selected_index = config_listbox.curselection()
    if selected_index:
        selected_index = selected_index[0]
        config_data = configurations[selected_index]
        custom_ip_entry.delete(0, tk.END)
        custom_ip_entry.insert(0, config_data.get("ip_address", ""))
        username_entry.delete(0, tk.END)
        username_entry.insert(0, config_data.get("username", ""))
        password_entry.delete(0, tk.END)
        password_entry.insert(0, config_data.get("password", ""))
        dbname_entry.delete(0, tk.END)
        dbname_entry.insert(0, config_data.get("dbname", ""))
        server_name_entry.delete(0, tk.END)
        server_name_entry.insert(0, config_data.get("server_name", ""))
    else:
        print("Please select a configuration to load.")


# Function to save current configuration
def save_current_config():
    server_name = server_name_entry.get().strip()
    ip_address = custom_ip_entry.get().strip()
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    dbname = dbname_entry.get().strip()

    if not server_name or not ip_address or not username or not password or not dbname:
        print("Please fill in all fields.")
        return

    # Check if server name already exists
    for config in configurations:
        if config.get("server_name") == server_name:
            # Handle duplicate server name (e.g., prompt user, update existing entry)
            print(f"Server name '{server_name}' already exists. Updating existing entry.")
            config.update({
                "ip_address": ip_address,
                "username": username,
                "password": password,
                "dbname": dbname
            })
            break
    else:
        # Add new configuration
        config_data = {
            "server_name": server_name,
            "ip_address": ip_address,
            "username": username,
            "password": password,
            "dbname": dbname
        }
        configurations.append(config_data)

    # Save configurations and update listbox
    save_configs()
    update_config_listbox()


# Function to delete selected configuration
def delete_config():
    selected_index = config_listbox.curselection()
    if selected_index:
        selected_index = selected_index[0]
        deleted_config = configurations.pop(selected_index)
        print(f"Deleted configuration: {deleted_config}")
        save_configs()  # Save updated configurations after deletion
        update_config_listbox()
    else:
        print("Please select a configuration to delete.")


# Function to handle database connection
def connect_to_database():
    ip_address = custom_ip_entry.get().strip()
    if not ip_address:
        print("Please enter IP address.")
        return

    username = username_entry.get().strip()
    password = password_entry.get().strip()
    dbname = dbname_entry.get().strip()

    if not username or not password or not dbname:
        print("Please fill in all fields.")
        return

    server_name = server_name_entry.get().strip()
    if not server_name:
        server_name = f"{ip_address}-{dbname}"  # Generate a default server name if not provided

    print(f"Connecting to {server_name} at IP address: {ip_address}")
    print(f"Username: {username}, Password: {password}, Database: {dbname}")

    # Implement your database connection logic here using the entered details
    # Optionally, save the configuration after successful connection
    save_current_config()


# Initialize configurations list
configurations = []

# Create GUI
root = tk.Tk()
root.title("Database Connection Setup")

# Create a frame for better organization
main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack()

# Server Name input
tk.Label(main_frame, text="Server Name:").grid(row=0, column=0, sticky=tk.W)
server_name_entry = tk.Entry(main_frame, width=30)
server_name_entry.grid(row=0, column=1)

# IP Address input
tk.Label(main_frame, text="Enter IP Address:").grid(row=1, column=0, sticky=tk.W)
custom_ip_entry = tk.Entry(main_frame, width=30)
custom_ip_entry.grid(row=1, column=1)

# Username input
tk.Label(main_frame, text="Username:").grid(row=2, column=0, sticky=tk.W)
username_entry = tk.Entry(main_frame, width=30)
username_entry.grid(row=2, column=1)

# Password input
tk.Label(main_frame, text="Password:").grid(row=3, column=0, sticky=tk.W)
password_entry = tk.Entry(main_frame, show="*", width=30)
password_entry.grid(row=3, column=1)

# Database name input
tk.Label(main_frame, text="Database Name:").grid(row=4, column=0, sticky=tk.W)
dbname_entry = tk.Entry(main_frame, width=30)
dbname_entry.grid(row=4, column=1)

# Configurations listbox
config_listbox = tk.Listbox(main_frame, selectmode=tk.SINGLE, width=40, height=10)
config_listbox.grid(row=0, column=2, rowspan=5, padx=(20, 0))

# Load saved configurations button
load_configs_button = tk.Button(main_frame, text="Load Configurations", command=load_configs)
load_configs_button.grid(row=5, column=2, sticky=tk.W, pady=(10, 0))

# Load selected configuration button
load_selected_button = tk.Button(main_frame, text="Load Selected", command=load_selected_config)
load_selected_button.grid(row=5, column=2, sticky=tk.E, pady=(10, 0))

# Save current configuration button
save_config_button = tk.Button(main_frame, text="Save Current", command=save_current_config)
save_config_button.grid(row=6, column=2, pady=(10, 0))

# Delete configuration button
delete_config_button = tk.Button(main_frame, text="Delete Selected", command=delete_config)
delete_config_button.grid(row=7, column=2, pady=(10, 0))

# Connect button
connect_button = tk.Button(main_frame, text="Connect", command=connect_to_database)
connect_button.grid(row=8, column=1, pady=(20, 0))

root.mainloop()
