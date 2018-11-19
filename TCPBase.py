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
