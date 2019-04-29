#! /usr/bin/python3
"""

This application gives demonstration of how to use external USB based GPS functions.
 
Note: GPS baudrate as well as GPS strings update rate can be configurable through mini GPS application.
This application works for the GPS with baudrate = 38400.

This application uses ctype foreign function library for python and that allows calling a functions from DLLs or shared libraries.  

"""
from __future__ import print_function
from ctypes import *
from array import *
import sys
import os
import socket
import struct
import sys
import time



peripheralBaudRate = c_ulong(38400)
MAXBUFFERSIZE = int(1000)
GPSSTRING_TYPE = (c_ubyte * MAXBUFFERSIZE)
gpsStringArray = GPSSTRING_TYPE()

class GPS_STRUCT(Structure):
    _fields_ = [("gpsLatitude", c_float),
                ("gpsLongitude", c_float),
                ("gpsDirection_NS", c_char),
                ("gpsDirection_EW", c_char),
                ("gpsSatLock", c_ubyte),
                ("gpsSatFix", c_ubyte)]

if sys.platform.startswith('win32'):
    ComPort = b"\\\\.\\COM3"
elif sys.platform.startswith('linux'):
    ComPort = b"/dev/ttyUSB0"

if sys.platform.startswith('win32'):
    libraryPATH = os.path.join(os.getcwd(),"FireBirdCLibrary.dll")
elif sys.platform.startswith('linux'):
    libraryPATH = os.path.join(os.getcwd(),"libFireBirdCLibrary.so")
    
lib = CDLL(libraryPATH)

def open_comport(Com,baudRate):
    hcomm = lib.connect_peripheral(Com,baudRate)
    return hcomm

hcomm = c_void_p(0)
gps_struct = GPS_STRUCT()




multicast_group = ('224.3.29.71', 10000)        #communication part
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(0.2)
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
#sent = sock.sendto(str(v).encode(), multicast_group)


hcomm = open_comport(ComPort,peripheralBaudRate)                                            #Open communication port
i = int(0)
if hcomm != 0:

    while True:
                               
        if lib.getGPSdata(hcomm,c_ulong(MAXBUFFERSIZE),gpsStringArray,byref(gps_struct)):
            for i in gpsStringArray:                                                        #Print string all strings received from GPS
                print (chr(i),end='')

            message = str(gps_struct.gpsLatitude)+"####"+str(gps_struct.gpsLongitude)+"####"+str((gps_struct.gpsDirection_NS).decode("utf-8"))+"####"+str((gps_struct.gpsDirection_EW).decode("utf-8"))+"####"+str(gps_struct.gpsSatLock)+"####"+str(gps_struct.gpsSatFix)
            sent = sock.sendto(str(message).encode(), multicast_group)
            print(message)
            print(message.split("####"))
            time.sleep(5)


            '''
            print('\n')
            print("Latitude = ",gps_struct.gpsLatitude)                                     #GPS latitude
            print("Longitude = ",gps_struct.gpsLongitude)                                   #GPS longitude
            print("Direction E/W = ",(gps_struct.gpsDirection_EW).decode("utf-8"))          #Direction East/West
            print("Direction N/S = ",(gps_struct.gpsDirection_NS).decode("utf-8"))          #Direction North/South
            print("No. of satellite locked = ",gps_struct.gpsSatLock)                       #GPS satellite lock
            print("No. of satellite fixed = ",gps_struct.gpsSatFix)                         #GPS satellite fix
            '''
     

        # sent = sock.sendto(str(0).encode(), multicast_group)

else:
    print ("CAN NOT ESTABLISH COMMUNICATION\n")    
    lib.disconnect_peripheral(hcomm)
    

