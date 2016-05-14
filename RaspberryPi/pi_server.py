#!/usr/bin/env python

# Install pyserial with command: pip install pyserial
import serial
import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Host 0.0.0.0 means to listen all ip address
server_address = ('0.0.0.0', 2015)
print >>sys.stderr, 'Starting up TCP Server. Server listening on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

# Plug arduino and scan port with command: ls /dev/tty*
ser = serial.Serial('/dev/ttyACM0', 115200)

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()

    try:
        print >>sys.stderr, 'connection from', client_address

        # Receive the data and transmit it to Arduino over serial usb
        while True:
            data = connection.recv(4096)
            print >>sys.stderr, 'received "%s"' % data
            ser.write(data)
            if not data:
                print >>sys.stderr, 'no more data from', client_address
                break

    finally:
        # Clean up the connection
        connection.close()
