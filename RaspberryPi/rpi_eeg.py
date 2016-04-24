#!/usr/bin/env python

__author__ = "Daro Oem"
__copyright__ = "Copyright 2016, The Mind-Controlled Robot Project"
__credits__ = ["Daro Oem"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = ""
__email__ = "oemdaro@gmail.com"
__status__ = "Educational"

import serial
# Plug arduino and scan port with command: ls /dev/tty*
ser = serial.Serial('/dev/ttyACM0', 115200)

while True:
    ser.readline()
