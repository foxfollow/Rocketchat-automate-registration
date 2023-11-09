import paramiko
import time
import re

def ssh_connection(ip, username, password):
    # Create an SSH client object
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the remote server
    ssh.connect(ip, username=username, password=password)

    # Execute the commands in the provided code block
    stdin, stdout, stderr = ssh.exec_command('''cat << EOF |sudo tee -a ./ip.py
import socket
import subprocess
import time


def autoChangeIpRocketChat(isForDeploy=True):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    if isForDeploy:
        ipToChange = s.getsockname()[0]
        ipFalsed = "localhost"
    else:
        ipToChange = "localhost"
        ipFalsed =  s.getsockname()[0]

    # ip = "10.10.20.32"

    while True:
        # Check the status of the service
        result = subprocess.run(["sudo", "service", "snap.rocketchat-server.rocketchat-server", "status"],
                                capture_output=True,
                                text=True)

        if ipFalsed in result.stdout:
            # If localhost exists in the output, set the site URL and restart the service
            subprocess.run(["sudo", "snap", "set", "rocketchat-server", f"siteurl=http://{ipToChange}:3000"], check=True)
            subprocess.run(["sudo", "service", "snap.rocketchat-server.rocketchat-server", "restart"], check=True)
            print("restarting")
        elif ipToChange in result.stdout:
            print(f"{ipToChange} exists in the output, break the loop")
            break
        else:
            # If neither localhost nor 10.10.20.33 exist in the output, wait for 10 seconds and repeat
            print("sleep 9")
            time.sleep(9)


autoChangeIpRocketChat(isForDeploy=True)

EOF

python3 ip.py
''')

    # Wait for the command to finish executing
    time.sleep(20)

    # Check the output of the command for the string "break the loop"
    count = 0
    while True:
        output = stdout.read().decode()
        if "break the loop" in output:
            ssh.close()
            return re.search(r'\d+\.\d+\.\d+\.\d+', output).group(0)
        elif count < 3:
            count += 1
            stdin, stdout, stderr = ssh.exec_command("python3 ip.py")
            time.sleep(20)

        else:
            ssh.close()
            return None
