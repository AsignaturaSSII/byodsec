class ClientThread(TCPBase):
    def __init__(self):
        super(ClientThread, self).__init__()

    def run(self):
        '''
        Client thread
        '''
        err = 0
        try:
            self.ssl_sock = ssl.wrap_socket(self.soc,
                                            ca_certs=ssl_certfile,
                                            cert_reqs=ssl.CERT_REQUIRED)
            print("Wrapped client socket for SSL")

            try:
                self.ssl_sock.connect((host, port))
                print("client socket connected\n")

                print("send message")
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
