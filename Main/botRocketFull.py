import rcRegistration
import multiSender

listIps = [31,32,33]

rcRegistration.parallelMainRegistration(listIps)
multiSender.parallelMainSender(listIps)
