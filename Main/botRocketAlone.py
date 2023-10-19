# for solo using one target
import rcRegistration
import multiSender
import socket

# third_aktet = socket.gethostbyname(socket.gethostname()).split('.')[2]
third_aktet = 33

rcRegistration.mainRegistration(third_aktet)
print("Starting twiceSender")
multiSender.twiceSender(third_aktet)
