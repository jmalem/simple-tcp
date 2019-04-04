#!/usr/bin/python

from packet2 import *
import socket
import sys
import os
import pickle

class Sender:
    def __init__(self, receiver_host_ip, receiver_port, file, mws, mss):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.seq = 0
        self.ack = 0

        self.receiver_host_ip = receiver_host_ip
        self.receiver_port = int(receiver_port)

        self.file = file
        self.mws = int(mws)
        self.mss = int(mss)

        self.start=0
        self.end=0 # current time

    def sendSYN(self):
        p = Packet('', 0, 0, 1, 0, 0)
        p = pickle.dumps(p)
        self.s.sendto(p,(self.receiver_host_ip, self.receiver_port))
        print "send the SYN"

    def listenSYNACK(self):
        (packet, address) = self.s.recvfrom(2048)
        packet = pickle.loads(packet)
        if (packet.flag_syn==1 and packet.flag_ack==1):
            print "stage_1 passed"
            return True
        else:
            return False
    def sendPacket(self, p):
        p=pickle.dumps(p)
        self.s.sendto(p, (self.receiver_host_ip, self.receiver_port))


    def listen(self):
        (packet, address) = self.s.recvfrom(2048)
        packet = pickle.loads(packet)
        return packet
##MAIN##
if(len(sys.argv)!=6):
    print"Usage: python sender.py <receiver_host_ip> <receiver_port> <file_name> <mws> <mss>"
    exit(1);

receiver_host_ip=sys.argv[1]
receiver_port=sys.argv[2]
file_name=sys.argv[3]
mws=sys.argv[4]
mss=sys.argv[5]
#gamma=sys.argv[6]
#pDrop=sys.argv[7]
#pDuplicate=sys.argv[8]
#pCorrupt=sys.argv[9]
#pOrder=sys.argv[10]
#maxOrder=sys.argv[11]
#pDelay=sys.argv[12]
#maxDelay=sys.argv[13]
#seed=sys.argv[14]

#Indicator
stage_0 = 0     # When waiting for SYNACK
stage_1 = 0     # When waiting for ACK
stage_2 = 0     # all data sent, now send FIN

all_data=[]     # all the data segment in bytes
timeline={}     # all the data sent and their timestamp (used for retransmission

sent=0  #segments of data sent (array index)
to_be_acked=0 #segments sent that has not been acked
not_acked=0 # bytes of the segments not been acked
file_size=os.stat(file_name).st_size

s = Sender(receiver_host_ip, receiver_port, file_name, mws, mss)


i=0
with open(file_name,"rb") as f:
    while(i<file_size):
        d=f.read(s.mss)
        all_data.append(d)
        #print len(all_data)
        i=i+len(d)



while True:
    if stage_0==0:
        s.sendSYN()
        stage_0=1


    if stage_0==1 and stage_1==0:
        if(s.listenSYNACK() is True):
            stage_1=1
            print "3 way handshake is established with receiver"

    if stage_1==1 and stage_2==0:
        # Instantiate new packet
        if(sent < len(all_data)):
            packet = Packet(all_data[sent], s.seq, s.ack, 0, 1, 0)
            
            s.sendPacket(packet)
            sent += 1
            to_be_acked+=1
            print "sent: {}".format(sent)
            
            received=s.listen()
            if received.ack > not_acked and received.flag_ack==1:
                not_acked = received.ack
                to_be_acked -= 1;
            if sent == len(all_data):
                stage_2=1
    if stage_2==1:
        print("stage2")
        packet = Packet('', s.seq, s.ack, 0, 0, 1)
        s.sendPacket(packet)
        received=s.listen()
        if (received.flag_fin==1 and received.flag_ack==1):
            print "finack received"
            s.ack += 1
            print "send one last ack"
            packet = Packet('', s.seq, s.ack, 0, 1, 0)
            s.sendPacket(packet)
            break

print "closing the socket"
s.s.close()
'''
        if(sent<len(all_data)):
            packet = Packet(all_data[sent], s.seq, s.ack, 0, 1, 0)
            s.seq+=len(all_data[sent])
            sent+=1
            to_be_acked+=1
            #later check for dropped packet here
            s.sendPacket(packet)
            print"sent"
            received=s.listen()
            if received.ack > not_acked and received.flag_ack==1:
                not_acked = received.ack
                to_be_acked -= 1;
        else:
            stage_2=1

    if stage_2==1:
        print "in stage 2"
        pass
'''
