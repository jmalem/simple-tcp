import socket
import struct
from exampleheader import *
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1',2500))
print "Server is listening"
while True:
    (msg, address) = s.recvfrom(2048)
    print(struct.unpack('!HHLLBBHHH', msg))
