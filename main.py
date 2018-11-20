'''


para generar el self-signed SSL key y certificate:

openssl genrsa 1024 > ssl_key
openssl req -new -x509 -nodes -sha1 -days 365 -key ssl_key > ssl_cert

'''
import time
import threading
import socket
import ssl
import sys

port = 2049
host = "192.168.0.101"

ssl_keyfile = "ssl_key"
ssl_certfile = "ssl_cert"


try:
    ipAddr = socket.gethostbyname(host)
    print ("IP = " + ipAddr)
except socket.gaierror:
    print ("Host name could not be resolved")

class TCPBase(threading.Thread):
    def __init__(self):
        self.soc = self.buildSocket()
        super(TCPBase, self).__init__()

    def buildSocket(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print ('Socket created')
        except socket.error as msg:
            print ('Failed to create socket Error code: ' + str(msg[0]) + ', Error message: ' + msg[1])
        return s

    def printErr(self, usrMsg, msg):
        print (usrMsg)
        print (usrMsg)


class ClientThread(TCPBase):
    def __init__(self):
        super(ClientThread, self).__init__()

    def run(self):
        '''
        Client thread
        '''
        print("cliente ###########################")
        err = 0
        try:
            self.ssl_sock = ssl.wrap_socket(self.soc,
                                            ca_certs=ssl_certfile,
                                            cert_reqs=ssl.CERT_REQUIRED)
            print("Wrapped client socket for SSL")

            try:
                self.ssl_sock.connect((host, port))
                print("#################bbbbb#########################\n")
                print("client socket connected\n")
                message = sys.stdin.readline() 
                self.ssl_sock.send(message)
                print("send message")
                print("#########aaaa#################################\n")
                self.ssl_sock.sendall("Twas brillig and the slithy toves")

            except socket.error as msg:
                self.printErr("Socket connection error in client: ")

            finally:
                self.ssl_sock.close()

        except socket.error as j:
            print(j, '<---------')
            print("SSL socket wrapping failed")

        self.soc.close()
        print("exit client")
        print("###########aaaaavvvv################")

class ServerThread(TCPBase):
    def __init__(self):
        super(ServerThread, self).__init__()

    def run(self):
        '''
        Server thread
        '''
        err = 0
        msg = None
        try:
            self.soc.bind((host, port))
            print ("Bind worked\n")
        except socket.error as msg:
            print ("Bind failed in server: " + str(msg[0]) + " Message " + msg[1])
            err = 1
        if not err:
            try:
                self.soc.listen(10)
            except socket.error as msg:
                print ("Listen failed: "  + str(msg[0]) + " Message " + msg[1])
                err = 1
        if not err:
            self.conn, self.addr = self.soc.accept()
            print ("Accepted client connection to address " + str(self.addr) + "\n")
            try:
                self.connstream = ssl.wrap_socket(self.conn, 
                                                  server_side=True,
                                                  certfile=ssl_certfile,
                                                  keyfile=ssl_keyfile, 
                                                  ssl_version=ssl.PROTOCOL_TLSv1
                                                  )
                print ("SSL wrap succeeded for sever")
            except socket.error as msg:
                if (msg != None) :
                    print ("SSL wrap failed for server: "  + str(msg[0]) + " Message " + msg[1])
                err = 1

            while True:
                data = self.connstream.recv(1024)
                if data:
                    print ("server: " + data)
                else:
                    break
        self.soc.close()
        self.connstream.close()
        print ("exit server")


def main():   
    print ("Hello world")
    client = ClientThread()
    server = ServerThread()
    server.start()
    client.start()
    while client.isAlive() and server.isAlive():
        '''
        Do nothing
        '''  
        time.sleep(0.100)
    print ("Main: that's all folks")


main()
