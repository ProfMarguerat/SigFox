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
    
	while True :
    		if len(sys.argv) == 3:
            		portName = sys.argv[2]
            		sgfx = Sigfox(portName)
    		else:
        		sgfx = Sigfox('/dev/ttyAMA0')
		
			#Recupere la temperature SigFox
			litTemp ="ATI26\n"
		    	print("Envoi de la chaine : %s" % litTemp)
		    	envoi=sgfx.ser.write(litTemp)    # Chaine envoyée à la carte
		        
		    	temperature=sgfx.ser.read(15)
                        temperature=temperature[5:10]    
		    	print("Température mesurée : %s" % temperature)
			tmpBreakout=temperature          # Extraction température
			print("Temperature transmise : %s" % tmpBreakout)
			    	
			# Lit la temperature du SoC
			print ("lecture température SoC")
			cmd = '/opt/vc/bin/vcgencmd measure_temp'
			socTemp = os.popen(cmd).readline().strip()
			print ("Temperature SoC mesurée : %s" % socTemp) 
			soc= socTemp[5]+socTemp[6]+socTemp[8]   # Extraction température
			print ("Température transmise : %s" % soc)

			#Recupere la tension
			litTension ="ATI28\n"
		    	print("Envoi de la chaine : %s" % litTension)
		    	envoi=sgfx.ser.write(litTension)    # Envoi de la chaine de caracteres
		    
		    	tension=sgfx.ser.read(15)    # On récupère les valeurs des tensions
		    	print("Tensions lues : %s" % tension)
			volt=tension[9:10]+tension[11:15]
			print("Tensions transmises : %s" % volt)


                        time.sleep(5)	     
		    	message = tmpBreakout + soc + volt   # Construction du message SigFox
			print ("message : %s" % message)
		    	#if len(sys.argv) > 1:
		    	#    message = "{0}".format(sys.argv[1])
		    	sgfx.sendMessage(message)
    	
			time.sleep(900) #mise en sommeil pendant 15 mn

