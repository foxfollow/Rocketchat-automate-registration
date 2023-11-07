# CC23

[//]: # (![Using]&#40;https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54&#41;)
![Current](https://img.shields.io/badge/Python-3.10-blue)
![Current](https://img.shields.io/badge/Rocket_Chat-6.4.5-red)

## Description
Currently working version 1.0.1
Main file is in `%project%\Main` 
- filename: `botRocketAlone.py` which is compiled with pyinstaller to `~dist\botRocketAloneDeploy.exe`
- `botRocketAlone.py` using three hidden modules: `selenium` `~\multiSender.py` and `~\rcRegistration.py` (also `socket` but it's built in)

## Building .exe
In ./Main run command: 

```
pyinstaller .\botRocketAlone.py --onefile --hidden-import selenium --hidden-import rcRegistration --hidden-import multiSender --icon=icon.ico --name botRocketAloneDeploy.exe
```

File will be in `CC23\Main\dist\botRocketAloneDeploy.py`

## TODO
- Resolved an Error when answer() launch first (add to registration() write first message in chat)
- Develop a parallel registration (if needed)

## Versions
This script have been tested on:
Python 3.10 and 3.11
Rocketchat 6.4.2

## License

The MIT License (MIT)

Copyright (c) 2022 Heorhii Savoiskyi d3f0ld@proton.me
