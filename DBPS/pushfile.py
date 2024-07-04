import paramiko
import scp


pi_address = '192.168.146.174'
pi_username = 'pi'
pi_password = 'admin'

# Connect to the server via SSH
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(pi_address, username=pi_username, password=pi_password)

# SCP the file to Raspberry Pi
with scp.SCPClient(ssh.get_transport()) as scp_client:
    scp_client.put('encodings.pickle', remote_path='/home/pi/Desktop/LABVISAGENTRY/RASPBERRYPi')

# Close SSH connection
ssh.close()
