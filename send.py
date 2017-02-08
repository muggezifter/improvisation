import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 3000
MESSAGE = "2 1;"

print "TCP target IP:", UDP_IP
print "TCP target port:", UDP_PORT
print "message:", MESSAGE

sock = socket.socket(socket.AF_INET, # Internet
             socket.SOCK_STREAM) # UDP
sock.connect((UDP_IP, UDP_PORT))

sock.send(MESSAGE)
sock.send(MESSAGE)
sock.send(MESSAGE)

