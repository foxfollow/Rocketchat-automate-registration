# C:\Users\h_savoiskyi\AppData\Roaming\Python\Python310\Scripts\pyinstaller.exe
# $env:Path += ";C:\\Users\\h_savoiskyi\\AppData\\Roaming\\Python\\Python310\\Scripts"
# pyinstaller .\botRocketAlone.py --onefile --hidden-import selenium --icon=icon.ico

# cat << EOF |sudo tee -a ./ip.py
import sys
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

# EOF
#
# python3 ip.py

# ############################
# Get the input text from the command line arguments
# input_text = " ".join(sys.argv[1:])
#
# # Print the input text to the console
# print(input_text)
#
# time.sleep(5)
