import paramiko
import scp
import json

with open('config.json') as config_file:
    config = json.load(config_file)

pi_address = config["raspberry_pi"]["host"]
pi_username = config["raspberry_pi"]["user"]
pi_password = config["raspberry_pi"]["password"]

# Connect to the server via SSH
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(pi_address, username=pi_username, password=pi_password)

# SCP the file to Raspberry Pi
with scp.SCPClient(ssh.get_transport()) as scp_client:
    scp_client.put('/Users/nageswaransundaraju/Desktop/Python/LABVISAGEENTRY-FYP/buzzer.txt', remote_path='/home/pi/Desktop')

# Close SSH connection
ssh.close()
