 $env:Path += ";C:\\Users\\h_savoiskyi\\AppData\\Roaming\\Python\\Python310\\Scripts"
$version = Read-Host "Enter version number"
$params = "--onefile --hidden-import selenium --hidden-import rcRegistration --hidden-import multiSender --hidden-import paramiko --hidden-import sshRocketCfg --icon=icon.ico "
$commandDep = "pyinstaller .\botRocketAlone.py $params --name botRocketAloneDeploy_v$version.exe"
$commandTest = "pyinstaller .\botRocketAloneTester.py $params --name botRocketAloneTester_v$version.exe"

Invoke-Expression $commandDep
Invoke-Expression $commandTest

Get-ChildItem -Path . -Filter *.exe.spec | Where-Object { $_.Name -notmatch $version } | Remove-Item -Force

#pyinstaller .\botRocketAloneTester.py --onefile --hidden-import selenium --hidden-import rcRegistration --hidden-import multiSender  --icon=icon.ico --name botRocketAloneTester_v114.exe