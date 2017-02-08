import socket
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 3000
MESSAGE = "60 180;"

print "TCP target IP:", UDP_IP
print "TCP target port:", UDP_PORT
print "message:", MESSAGE

sock = socket.socket(socket.AF_INET, # Internet
             socket.SOCK_STREAM) # TCP
sock.connect((UDP_IP, UDP_PORT))
sock.send("60 580;")
time.sleep(2)
sock.send("60 0;")
time.sleep(0.5)
sock.send("61 580;")
time.sleep(2)
sock.send("61 0;")
time.sleep(0.5)
sock.send("62 580;")
time.sleep(2)
sock.send("62 0;")
time.sleep(0.5)
sock.send("63 580;")
time.sleep(2)
sock.send("63 0;")
time.sleep(0.5)
sock.send("64 580;")
time.sleep(2)
sock.send("64 0;")
time.sleep(0.5)
sock.send("65 580;")
time.sleep(2)
sock.send("65 0;")
time.sleep(0.5)
sock.send("66 580;")
time.sleep(2)
sock.send("66 0;")
time.sleep(0.5)
sock.send("67 580;")
time.sleep(2)
sock.send("67 0;")
time.sleep(0.5)
sock.send("68 580;")
time.sleep(2)
sock.send("68 0;")
time.sleep(0.5)
sock.send("69 580;")
time.sleep(2)
sock.send("69 0;")
time.sleep(0.5)
sock.send("70 580;")
time.sleep(2)
sock.send("70 0;")
time.sleep(0.5)
sock.send("71 580;")
time.sleep(2)
sock.send("71 0;")





