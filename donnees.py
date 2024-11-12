import time
import serial
import sys
from time import sleep
 
 
gpgll_info = "$GPGLL,"
gpsdata = []

def __init__(self, port):
        
        portName = '/dev/ttyACM0'
 
        print 'Serial port : ' + portName
        self.ser = serial.Serial("/dev/ttyACM0"),
            port=portName,
            baudrate=4800,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )
        
while True :
    
c = (str)(self.ser.readline())
GPGLL_data_available = c.find(gpgll_info)
    if GPGLL_data_available>0:
        gpsdata = c.split("GPGLL,",1)[1]
        currentMsg += gpsdata
        fichier = open("gpsdata.txt")
        fichier.write(gpsdata)
        fichier.close()