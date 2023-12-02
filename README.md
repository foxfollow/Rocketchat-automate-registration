# CC23 automatic web registration of rocketchat servers

[//]: # (![Using]&#40;https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54&#41;)
![Current](https://img.shields.io/badge/Python-3.10-blue)
![Current](https://img.shields.io/badge/Rocket_Chat-6.4.5-red)

## Description

### Foreword
Script is used to automate rocket chat registration using selenium and to spam messages to check if server is alive. Run the script with validate ip address and credentails (in `rcRegistration.py`), to register rocketchat and update setting (modify LDAP configs on rocketchat server and disable two-factor auth)

### Notations
Currently working version of self 1.3.0

Main file is in `%project%\Main` 
- filename: `botRocketAlone.py` which is compiled with pyinstaller to .exe -> `~dist\botRocketAloneDeploy.exe`

- `botRocketAlone.py` using four hidden modules: 
    - `selenium`: This is a powerful tool for controlling a web browser through the program. It's used in this script to automate browser tasks such as navigating to a URL, interacting with the page elements, or even checking if the page is empty.

    - `multiSender.py`: This module is responsible for sending messages from different sessions. It could be used for testing the chat server's ability to handle multiple simultaneous messages.

    - `rcRegistration.py`: This module handles the registration process for the chat server. It automate the process of setup LDAP for users registration via domain controller. 

    - `sshRocketCfg.py`: This module provides functionality for SSH session. It could be used to remotely control servers, for example to start or stop the chat server, or to modify its configuration.

    - `paramiko`: This is a Python implementation of the SSHv2 protocol, which provides client and server functionality. While it's not a hidden module in the traditional sense, it's a crucial part of the sshRocketCfg.py module, as it provides the underlying SSH functionality.

## How to use

### Required changes
1. Change the row in file `botRocketAlone.py` (in my env rocket chat machines have fourth octet same as third in windows machine witch running the script, but you use full ip manual changing in `rcRegistration.py` - `serverIP` or remake it for your needs)
```
thirdOctet = socket.gethostbyname(socket.gethostname()).split('.')[2]     # FOR DEPLOY
```

2. Change the row in file `rcRegistration.py`
```python
domainPassword = 'SCP.Admin1' # password for domain user to access LDAP finding users

...

def getValues(isDeploy, thirdOctet):
    strOctet = str(thirdOctet)
    if not isDeploy:
        variables = {
            'serverIP': f'10.10.20.{strOctet}', # ip of rocket chat
            'domainIP': '10.10.20.30',  # ip of domain controller
            'domainDN': 'DC=rct,DC=local',  # where to find users
            'domainUser': f'CN=Administrator,CN=Users,DC=rct,DC=local', # domain user DN (to find users for ldap auth)
            'myMail': "s.g.d3f0ld@gmail.com" # mail acount for activation rocket chat (letter will be sended here for step setup 4)
        }
    else:
        if int(thirdOctet) < 10:
            zeroOctet = "0" + strOctet
        else:
            zeroOctet = strOctet
        variables = {
            'serverIP': f'198.18.96.{strOctet}',  # ip of rocket chat
            'domainIP': f'10.122.{strOctet}.113', # ip of domain controller
            'domainDN': f'DC=spectrum,DC={zeroOctet},DC=power,DC=cc23', # where to find users
            'domainUser': f'CN=SCPAdmin,CN=Users,DC=spectrum,DC={zeroOctet},DC=power,DC=cc23', # domain user DN (to find users for ldap auth)
            'myMail': "h.training.scpc@gmail.com"  # mail acount for activation rocket chat (letter will be sended here for step setup 4)
        }
    return variables

...

    sshRocketCfg.ssh_connection(ip, "root", "Admin1Admin1")     # local creds for chatserver shell 

...
    # future cred to admin account in web rocketchat
    doSendKeys(driver, By.NAME, 'fullname', 'chat-admin')

    doSendKeys(driver, By.NAME, 'username', 'chat-admin')


    doSendKeys(driver, By.NAME, 'email', variables['myMail'])

    password_elem = doSendKeys(driver, By.NAME, 'password', 'P@ssw0rd')

...

    #if changed future creds change also all this lines including in multiSender.py
    tmpLogin(driver, "chat-admin", "P@ssw0rd")

```

3. `multiSender.py` - used for sending spam messages, schedule 2 messages for 1 min (check if server is alive)
```python
# names of users in ldap
username1 = "operator1" 
username2 = "operator2"

...

# change passwords in both functions def answer(url_server): and def sender(url_server):

if not login(driver, f"{username1}@rct.local", "Admin1Admin1"): # change only password if you do not chage domainDefault = "rct.local" in rcRegistration.py
    login(driver, username1, "Admin1Admin1") #change password if needed

...

# also remake if you do not use octet, and change halfIP
def mainDeploySender(octet, index):
    halfIp = '198.18.96.'   # change ip
    
def mainTestSender(octet, index):
    halfIp = '10.10.20.' # change ip

```

4. Build your script - next paragraph
## Building .exe
In ./Main run command: 

```
pyinstaller .\botRocketAlone.py --onefile --hidden-import selenium --hidden-import rcRegistration --hidden-import multiSender --hidden-import paramiko --hidden-import sshRocketCfg --icon=icon.ico --name botRocketAloneDeploy.exe
```
### Anouther way is building
in In ./Main run `build.ps1`;
Enter the version ex: `130` (for 1.3.0) it will be added at the end of file name, than select `d` option for deploy

File will be in
```
CC23\Main\dist\botRocketAloneDeploy_v130.py
```

## Versions
This script have been tested on:
Python 3.10
Rocketchat 6.4.5

## License

The MIT License (MIT)

Copyright (c) 2022 Heorhii Savoiskyi d3f0ld@proton.me
