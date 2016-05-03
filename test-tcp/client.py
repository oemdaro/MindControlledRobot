#!/usr/bin/env python

import socket
import sys
import time

message = ['This is the message. Send from client "127.0.0.1" on port "2016"',
                'This is a second message. Send from client "127.0.0.1" on port "2016"']
i = 0

while True:
    try:
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        server_address = ('localhost', 2016)
        print >>sys.stderr, 'connecting to %s port %s' % server_address
        sock.connect(server_address)
        # Send data
        print >>sys.stderr, 'sending "%s"' % message[i]
        sock.sendall(message[i])
        i = i + 1
        if i >= 2:
            i = 0
        time.sleep(2)

        # Look for the response
        # amount_received = 0
        # amount_expected = len(message)
        # # #
        # while amount_received < amount_expected:
        #     data = sock.recv(4096)
        #     amount_received += len(data)
        #     print >>sys.stderr, 'received "%s"' % data
        #     time.sleep(2)
        #     if data == "w":
        #         print "Recieved W"

    finally:
        print >>sys.stderr, 'closing socket'
        sock.close()
