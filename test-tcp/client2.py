import socket

#----------------------------------------------------------------------
def sendSocketMessage(message):
    """
    Send a message to a socket
    """
    try:
        client = socket.socket(socket.AF_INET,
                               socket.SOCK_STREAM)
        client.connect(('localhost', 2016))
        client.send(message)
        client.shutdown(socket.SHUT_RDWR)
        client.close()
    except Exception, msg:
        print msg

if __name__ == "__main__":
    sendSocketMessage("Python rocks!")
