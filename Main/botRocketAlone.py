# for solo using one target
import rcRegistration
import multiSender
import socket
import sys

thirdOctet = socket.gethostbyname(socket.gethostname()).split('.')[2]     # FOR DEPLOY
# thirdOctet = "35"     # FOR TESTER
# thirdOctet = sys.argv[1]             # FOR TESTER

rcRegistration.mainRegistration(thirdOctet, isDeploy=True)
multiSender.logToFile("Starting multiSender.twiceSender", scriptName="botRocketAlone.py")
multiSender.twiceSender(thirdOctet, isDeploy=True)
multiSender.logToFile("Script ended", scriptName="botRocketAlone.py")
