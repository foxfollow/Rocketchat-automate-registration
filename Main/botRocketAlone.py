# for solo using one target
import time
import rcRegistration
import multiSender
import socket
import sys

thirdOctet = socket.gethostbyname(socket.gethostname()).split('.')[2]     # FOR DEPLOY
# thirdOctet = "35"     # FOR TESTER
# thirdOctet = sys.argv[1]             # FOR TESTER

multiSender.logToFile("version botRocketAlone.py - 1.3.0", scriptName="botRocketAlone.py")

while True:
    try:
        rcRegistration.mainRegistration(thirdOctet, isDeploy=True)
        multiSender.logToFile("Starting multiSender.twiceSender", scriptName="botRocketAlone.py")
        multiSender.twiceSender(thirdOctet, isDeploy=True)
        multiSender.logToFile("Script ended", scriptName="botRocketAlone.py")
        break
    except Exception as e:
        multiSender.logToFile(f"Error occurred: {e}", scriptName="botRocketAlone.py")
        multiSender.logToFile("Restarting in 10 minutes...", scriptName="botRocketAlone.py")
        time.sleep(600)
