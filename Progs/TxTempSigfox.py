#!/usr/bin/env python
# -*- coding: utf-8 -*-
## @package rpisigfox
#  Ce script contrôle la carte BRKWS01 pour l'envoi d'un message SIGFOX.
#
#  V1.0 Permet l'envoi d'un message normal sur le réseau SigFox.
#  syntaxe :
#  ./tx.py MESSAGE
#  où MESSAGE est une chaîne encodée en HEXA. La longueur peut être de 2 à 24 caractères représentant 1 à 12 octets.
#  Exemple : ./tx.py 00AA55BF envoie les 4 octets 0x00 0xAA 0x55 0xBF
#
import time
import serial
import sys
from time import sleep
from envirophat import weather, leds

temp = 0

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
        while iterCount >= 0 and success not in currentMsg and  failure not in currentMsg :
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
            if self.WaitFor('OK', 'ERROR', 15) :
                print('OK Message envoyé')

        else:
            print 'Erreur Modem SigFox'

        self.ser.close()

if __name__ == '__main__':

    leds.on()
    time.sleep(0.5)    
    leds.off()

    temperature = float (weather.temperature())
    temp = temperature
    

    print("{} degrees Celsius".format(temp))   

    if len(sys.argv) == 3:
        portName = sys.argv[2]
        sgfx = Sigfox(portName)
    else:
        sgfx = Sigfox('/dev/ttyAMA0')

    message = temp
    if len(sys.argv) > 1:
        message = "{0}".format(sys.argv[1])

    sgfx.sendMessage(message)
       
    #time.sleep(30) #mise en sommeil pendant 10 mn
