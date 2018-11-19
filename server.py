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
