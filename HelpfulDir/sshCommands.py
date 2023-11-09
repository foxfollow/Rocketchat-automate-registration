import time
import paramiko


def ssh_command(octet, username, passwd, myCommand):
    ip = f'10.122.{octet}.123'
    # key = paramiko.RSAKey(filename=passwd)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=username, password=passwd)
    stdin, stdout, stderr = client.exec_command(myCommand)
    print(f"output for commands {myCommand}", stdout.read(), f"for team number {octet}")
    client.close()


# List of IPs
#  = ['198.18.96.2', '198.18.96.4']
octets = '2|4|5|6|7|9|10|12|14|16|17|18|19|24|26|27|29|31|32|34|35|36|39|40'.split("|")
# octets = ['2']
# SSH details
linuxUser = 'root'
windowsUser = 'Administrator'
ssh_key_filepath = '/home/fox/.ssh/id_cc23.key'

# Command to execute
# linuxCommand = 'echo "flag {12345654321}" > /etc/connection_check.txt; cat /etc/connection_check.txt'
linuxCommand = 'cat /etc/connection_check.txt'
windowsCommand = 'echo "flag {12345654321}" | Out-File -FilePath C:\\connection_check.txt; cat C:\\connection_check.txt'

passwd = 'Admin1Admin1'

for ip in octets:
    ssh_command(ip, windowsUser, passwd, windowsCommand)
    time.sleep(1)
