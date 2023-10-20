# for solo using one target
import rcRegistration
import multiSender
import socket

thirdOctet = socket.gethostbyname(socket.gethostname()).split('.')[2]
# third_aktet = 33

rcRegistration.mainRegistration(thirdOctet, isDeploy=True)
print("Starting twiceSender")
multiSender.twiceSender(thirdOctet, isDeploy=True)
