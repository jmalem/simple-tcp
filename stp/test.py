from packet import *

p=Packet("a",2000,2501,'127.0.0.1')
p.calculate_checksum()
print p.checksum

p1=Packet("a",2000,2501,'127.0.0.1')
p1.calculate_checksum()
print p1.checksum

p2=Packet("asdsdds",2000,2800,'102.192.0.1')
p1.calculate_checksum()
print p1.checksum
