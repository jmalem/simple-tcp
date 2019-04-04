import socket
import struct
import pickle

class Packet:
    def __init__ (self, data, src_port, dest_port, dest_ip):
        self.data = data
        self.src_port = src_port
        self.dest_port = dest_port
        self.dest_ip = dest_ip
        self.src_ip='127.0.0.1'
        self.seq=0
        self.seq_ack=0
        self.hlen=0
        self.window=0
        self.flag=self.setFlag('A')

        self.header=None
        self.checksum=self.calculate_checksum()

    def setFlag(self,type):
        if(type=='S'):
            self.flag=bin(0)
        elif(type=='A'):
            self.flag=bin(1)
        elif(type=='D'):
            self.flag=bin(2)
        elif(type=='F'):
            self.flag=bin(3)
        self.checksum=self.calculate_checksum()
    def createHeader(self):
        #count the check Sum
        #self.header=struct.pack('!s',"TEST INPUT ONLY")
        self.header=pickle.dumps((self.src_port,self.dest_port,self.src_ip,self.dest_ip))
        #set the Flags

        #create Packet
        return

    def calculate_checksum(self):
        #making the pseudo header
        #convert to 32 bits
        src_adrress=socket.inet_aton(self.src_ip)
        dest_adrress=socket.inet_aton(self.dest_ip)
        reserve=0
        protocol= socket.IPPROTO_UDP
        length=len(self.data)
        self.createHeader()
        pseudo=pickle.dumps((self.header,reserve,protocol,length,self.seq,
        self.seq_ack,self.hlen,self.window,self.flag))

        csum=bin(0)
        csum = 0  # Binary Sum

        # loop taking 2 characters at a time
        for n in range(1, len(pseudo), 2):

         a = ord(pseudo[n-1])
         b = ord(pseudo[n])
         csum = csum + (a+(b << 8))


        # One's Complement
        csum = csum + (csum >> 16)
        csum = ~csum & 0xffff
        return csum
