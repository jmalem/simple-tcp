import socket
import struct
import pickle
import time
from packet import *

s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1',2501))

def send_reply(socket,dest_ip,dest_port,src_ip,src_port):
    socket.sendto("reply", ('127.0.0.1',2000))

print "Server is listening"
try:
    while True:
        (msg, address) = s.recvfrom(2048)
        (dest_port,src_port,dest_ip,src_ip)=(pickle.loads(msg))
        print "Im going to reply from port ",src_port
        print "Im sending my reply to port ",dest_port
        time.sleep(2)
        print "sending now"
        #send_reply(s,dest_ip,dest_port,src_ip,src_port)
        s.sendto("TESTREPLY",address)
except(KeyboardInterrupt):
    s.close()
    exit()
