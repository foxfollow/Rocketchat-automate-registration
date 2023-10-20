# for solo using one target
import rcRegistration
import multiSender
import socket
import sys

thirdOctet = socket.gethostbyname(socket.gethostname()).split('.')[2]
# thirdOctet = sys.argv[1]

rcRegistration.mainRegistration(thirdOctet, isDeploy=True)
print("Starting twiceSender")
multiSender.twiceSender(thirdOctet, isDeploy=True)
