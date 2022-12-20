#!/usr/bin/python
# -*- coding: utf-8 -*-

# Lecture de valeurs analogiques par un MCP3008 branché au Raspberry Pi
# Un potentiomètre est branché au canal 0 du MCP3008, un autre est branché
# au canal 1.
# http://electroniqueamateur.blogspot.com/2014/03/lecture-de-capteurs-analogiques-sur-le.html
 
import spidev
import time
 
# Ouverture du bus SPI
spi = spidev.SpiDev()
spi.open(0,0)  # car j'utilise la pin CE0:  serait spi.open(0,1) si j'utilisais la pin CE1
spi.max_speed_hz=1000000  # maintenant nécessaire pour que ça fonctionne
 
# Fonction qui lit l'information en provenance du MCP3008
# L'argument channel est le numéro de canal du MCP3008:  entier de 0 à 7
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  print("adc : ", adc)
  data = ((adc[1]&3) << 8) + adc[2]
  return data

 
while True:
 
  # Lecture du premier capteur, branché au canal 0 du MCP3008
  valeur1 = ReadChannel(0)
 
  # Lecture du deuxième capteur, branché au canal 1 du MCP3008
#   valeur2 = ReadChannel(1)

  # Affichage des résulats à l'écran
  print( "Valeur 1: " + str( valeur1 ) )
 
  # Pause syndicale:  on attend une seconde avant la prochaine prise de mesure.
  time.sleep(0.5)