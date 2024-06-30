import paramiko
import scp


pi_address = '192.168.0.9'
pi_username = 'root'
pi_password = 'admin'

# Connect to the server via SSH
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(pi_address, username=pi_username, password=pi_password)

# SCP the file to Raspberry Pi
with scp.SCPClient(ssh.get_transport()) as scp_client:
    scp_client.put('file_name', remote_path='pathname/')

# Close SSH connection
ssh.close()
