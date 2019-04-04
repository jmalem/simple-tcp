from packet import *
import socket
import threading
import sys

def send_reply(socket,dest_ip,dest_port,src_ip,src_port):
    socket.sendto("reply", (dest_ip,dest_port))


class Sender:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.src_port=2000
        self.dest_port=2501
        self.src_ip='127.0.0.1'
        self.dest_ip='127.0.0.1'
#create the packet containing header only to send a SYN

    def sendSyn(self):
        p=Packet('tes',self.src_port,self.dest_port,'127.0.0.1')
        p.createHeader()
        self.s.sendto(p.header,('127.0.0.1',self.dest_port))

    def listen(self):
        print "IM HERE"
                
        msg = self.s.recv(4096)
        print "the data is %s" %(msg)

if __name__ == '__main__':

    #receiver_host_ip=sys.argv[1]
    #receiver_port=sys.argv[2]
    #file=sys.argv[3]
    #mws=sys.argv[4]
    #mss=sys.argv[5]
    #gamma=sys.argv[6]
    #pDrop=sys.argv[7]
    #pDuplicate=sys.argv[8]
    #pCorrupt=sys.argv[9]
    #pOrder=sys.argv[10]
    #maxOrder=sys.argv[11]
    #pDelay=sys.argv[12]
    #maxDelay=sys.argv[13]
    #seed=sys.argv[14]

    sender=Sender()
    t2=threading.Thread(target=sender.listen)
    t2.start()
    sender.sendSyn()
