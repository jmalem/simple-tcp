#!/usr/bin/python

from packet2 import *
import socket
import sys
import os
import pickle

class Receiver:
    def __init__ (self, port):
        self.port = int(port)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(('127.0.0.1',self.port))
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.dest_ip = 0
        self.dest_port = 0
        self.ack = 0
        self.seq = 0
        
    def listen(self):
        (packet, address) = self.s.recvfrom(2048)
        packet = pickle.loads(packet)
        if(packet.flag_syn==1):
            print "received syn"
            stage_0=1
            self.dest_ip = address[0]
            self.dest_port = address[1]
        return packet

    def writeData(self, packet):
        with open('file_r.pdf','a') as w:
                w.write(packet.payload)
    def sendSYNACK(self):
        p = Packet('', 0, 0, 1, 1, 0)
        p = pickle.dumps(p)
        self.s.sendto(p,(self.dest_ip, self.dest_port))

    def sendPacket(self, packet):
        packet = pickle.dumps(packet)
        self.s.sendto(packet,(self.dest_ip, self.dest_port))
# MAIN
if(len(sys.argv)!=2):
    print"Usage: python sender.py <receiving_port_numbers>"
    exit(1);

receiver_port=sys.argv[1]
r = Receiver(receiver_port)

stage_0 = 0     # waiting for SYN
stage_1 = 0     # waiting for ACK
stage_2 = 0     # waiting for FIN
with open('file_r.pdf','w') as w:
    pass

while True:
    #listen for syn
    if(stage_0==0):
        print "Listening to SYN"
        r.listen()
        stage_0=1
        r.ack += 1
        print "Received SYN\n"
    #send synack
    if(stage_0==1 and stage_1==0):
        print "dest port is {}".format(r.dest_port)
        print "Sent SYNACK to the initiating sender"
        r.sendSYNACK()
        r.seq += 1
        stage_1=1
        print "Listening to ACK"

    # first ack received
    # connection is established with sender
    if stage_1==1 and stage_2==0:
        p=r.listen()
        r.ack += len(p.payload)
        if(p.flag_ack==1 and p.flag_fin==0):
            print "ACK_NUM: {0}".format(r.ack)
            r.writeData(p)
            reply = Packet('', r.seq, r.ack)
            r.sendPacket(reply)
            #update log
            r.seq += len(reply.payload)
            
            # update log
        elif(p.flag_fin==1):
            print "FIN received, starting to close connection"
            r.ack+=1
            stage_2=1
            
    if stage_2==1:
        # send a fin ack
        print"AYY"
        p = Packet('',r.seq,r.ack,0,1,1)
        r.sendPacket(p)
        print "sent finack"
        received=r.listen()
        if(received.flag_ack==1):
            print"finack acknowledged, close connection"
            break

r.s.close()
