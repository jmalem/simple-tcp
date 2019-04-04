from exampleheader import *

if __name__=='__main__':
        # Create Raw Socket
 s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 tcp = TCPPacket()
 tcp.assemble_tcp_feilds()

 s.sendto(tcp.raw, ("127.0.0.1" , 2500 ))
