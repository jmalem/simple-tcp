import thread
import threading
import time
import socket


# def myfunc(name, delay):
#     print name
#     sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
#
# try:
#     thread.start_new_thread(myfunc,("Thread1",2))
#     thread.start_new_thread(myfunc,("Thread2",4))
# except:
#     print"unable to start thread"+"  asdasd"
# while 1:
#    pass


class Server:
    def __init__(self, portNum):
        print "Server Created with ip address 127.0.0.1 and port number %s" %portNum
        self.sc=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sc.bind(('127.0.0.1',portNum)) #bind the socket into local host and listen at port 2000
        self.portNum=portNum
        self.clients=[]

    def listen(self):
        print "Listening at port %s" %self.portNum
        while True:
            (msg, client) = self.sc.recvfrom(1024)
            print tuple((msg,client))
            #self.sc.close()

if __name__ == "__main__":
    serv=Server(2000)
    serv.listen()
