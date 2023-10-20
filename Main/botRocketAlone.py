# for solo using one target
import rcRegistration
import multiSender
import socket

thirdOctet = socket.gethostbyname(socket.gethostname()).split('.')[2]
# third_aktet = 33

rcRegistration.mainRegistration(thirdOctet, isDeploy=False)
print("Starting twiceSender")
multiSender.twiceSender(thirdOctet, isDeploy=False)
