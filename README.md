# CC23

[//]: # (![Using]&#40;https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54&#41;)
![Current](https://img.shields.io/badge/Python-3.10-blue)
![Current](https://img.shields.io/badge/Rocket_Chat-6.4.5-red)

## Description

Currently working version of self 1.3.0

Main file is in `%project%\Main` 
- filename: `botRocketAlone.py` which is compiled with pyinstaller to .exe -> `~dist\botRocketAloneDeploy.exe`

- `botRocketAlone.py` using four hidden modules: 
    - selenium: This is a powerful tool for controlling a web browser through the program. It's used in this script to automate browser tasks such as navigating to a URL, interacting with the page elements, or even checking if the page is empty.

    - multiSender.py: This module is responsible for sending messages from different sessions. It could be used for testing the chat server's ability to handle multiple simultaneous messages.

    - rcRegistration.py: This module handles the registration process for the chat server. It automate the process of setup LDAP for users registration via domain controller. 

    - sshRocketCfg.py: This module provides functionality for SSH session. It could be used to remotely control servers, for example to start or stop the chat server, or to modify its configuration.

    - paramiko: This is a Python implementation of the SSHv2 protocol, which provides client and server functionality. While it's not a hidden module in the traditional sense, it's a crucial part of the sshRocketCfg.py module, as it provides the underlying SSH functionality.



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

## TODO
- Develop a parallel registration (if needed)

## Versions
This script have been tested on:
Python 3.10
Rocketchat 6.4.5

## License

The MIT License (MIT)

Copyright (c) 2022 Heorhii Savoiskyi d3f0ld@proton.me
