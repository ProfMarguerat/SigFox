#!/usr/bin/python
# -*- coding: utf-8 -*-

## @package rpisigfox
#  Ce script contrôle la carte BRKWS01 pour l'envoi d'un message SIGFOX.
#
#  V1.0 Permet l'envoi d'un message normal sur le réseau SigFox.
#  syntaxe :
#  ./tx.py MESSAGE 
#  où MESSAGE est une chaîne encodée en HEXA. La longueur peut être de 2 à 24 caractères représentant 1 à 12 octets.
#  Exemple : ./tx.py 00AA55BF envoie les 4 octets 0x00 0xAA 0x55 0xBF
# Sans paramètre c'est la chaine de mesure qui est utilisée

import time
import serial
import sys
import os
from time import sleep

porto = "/dev/ttyACM0"



class Sigfox(object):
    SOH = chr(0x01)
    STX = chr(0x02)
    EOT = chr(0x04)
    ACK = chr(0x06)
    NAK = chr(0x15)
    CAN = chr(0x18)
    CRC = chr(0x43)

    def __init__(self, port):
        # permet de choisir le port série – par défaut /dev/ttyAMA0
        portName = port
        
        print 'Serial port : ' + portName
        self.ser = serial.Serial(
                port=portName,
                baudrate=9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
        )

    def getc(self, size, timeout=1):
        return ser.read(size)

    def putc(self, data, timeout=1):
        ser.write(data)
        sleep(0.001) # temporisation pour permettre au circuit de se préparer

    def WaitFor(self, success, failure, timeOut):
        return self.ReceiveUntil(success, failure, timeOut) != ''

    def ReceiveUntil(self, success, failure, timeOut):
            iterCount = timeOut / 0.1
            self.ser.timeout = 0.1
            currentMsg = ''
            while iterCount >= 0 and success not in currentMsg and failure not in currentMsg :
                    sleep(0.1)
                    while self.ser.inWaiting() > 0 : # bunch of data ready for reading
                            c = self.ser.read()
                            currentMsg += c
                    iterCount -= 1
            if success in currentMsg :
                    return currentMsg
            elif failure in currentMsg :
                    print 'Erreur (' + currentMsg.replace('\r\n', '') + ')'
            else :
                    print 'Délai de réception dépassé (' + currentMsg.replace('\r\n', '') + ')'
            return ''

    def sendMessage(self, message):
        print 'Sending SigFox Message...'
        
        if(self.ser.isOpen() == True): # sur certaines plateformes il faut d'abord fermer le port série 
            self.ser.close()

        try:
            self.ser.open()
        except serial.SerialException as e:
            sys.stderr.write("Ouverture du port série impossible {}: {}\n".format(ser.name, e))
            sys.exit(1)

        self.ser.write('AT\r')
        if self.WaitFor('OK', 'ERROR', 3) :
                print('SigFox Modem OK')

                self.ser.write("AT$SF={0}\r".format(message))
                print('Envoi des données ...')
                if self.WaitFor('OK', 'ERREUR', 15) :
                        print('OK Message envoyé')

        else:
                print 'Erreur Modem SigFox'

        self.ser.close()
		





if __name__ == '__main__':

#        toto = serial.Serial(porto, baudrate = 4800, timeout = 0.5)


    
	while True :
                toto = serial.Serial(porto, baudrate = 4800, timeout = 0.5)
                data = toto.readline()
                while  data[0:6] != "$GPGGA":
                    data = toto.readline()
                if data[0:6] == "$GPGGA":
                    s = data.split(",")
                    if s[5] == "E":
                        t = s[2] + s[3] + s[4] + s[5]
                        t = t[0:4]+t[5:8]+t[12:16]+t[17:21]+t[22]
                    else :
                        t = s[2] + s[3] + s[4]
                        t = t[0:4]+t[5:9]+t[12:16]+t[17:21]

                    print s[2],s[3],s[4],s[5]
                    print t

    		if len(sys.argv) == 3:
            		portName = sys.argv[2]
            		sgfx = Sigfox(portName)
    		else:
        		sgfx = Sigfox('/dev/ttyAMA0')
                        
                       		
                        time.sleep(5)
                        message = t	     
			print ("message : %s" % message)
		    	sgfx.sendMessage(message)
    	
			time.sleep(120) #mise en sommeil pendant 15 mn

