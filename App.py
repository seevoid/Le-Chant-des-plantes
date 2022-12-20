from threading import Thread
from threading import Event

from gpiozero import MCP3008

import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

from signal import signal, SIGINT
from sys import exit

import random

import time
import fluidsynth

from bisect import bisect_left

VOLUME_ACCORDS = 30

NULL_VALUE_VOLT = 0.0004885197850512668

GAMME_MINEUR_BLUES_LA = [0,2,3,4,7,9]
GAMME_MAJEUR_LA = [1,2,4,6,8,9,11]
GAMME_MINEUR_BLUES_DO = [0,3,5,6,7,10]


CHOOSEN_GAMME = GAMME_MINEUR_BLUES_LA

def take_closest(myList, myNumber):
	"""
	Assumes myList is sorted. Returns closest value to myNumber.

	If two numbers are equally close, return the smallest number.
	"""
	pos = bisect_left(myList, myNumber)
	if pos == 0:
		return myList[0]
	if pos == len(myList):
		return myList[-1]
	before = myList[pos - 1]
	after = myList[pos]
	if after - myNumber < myNumber - before:
	   return after
	else:
	   return before

def handler(signal_received, frame):
	global plant_1
	global plant_2
	global accords
	# Handle any cleanup here
	print('SIGINT or CTRL-C detected. Exiting gracefully')
	plant_1.stop = True
	plant_1.join()
	plant_2.stop = True
	plant_2.join()
	accords.join()
	exit(0)

class ThreadWithReturnValue(Thread):
	def __init__(self, group=None, target=None, name=None,
				 args=(), kwargs={}, Verbose=None):
		Thread.__init__(self, group, target, name, args, kwargs)
		self._return = None
	def run(self):
		if self._target is not None:
			self._return = self._target(*self._args,
												**self._kwargs)
	def join(self, *args):
		Thread.join(self, *args)
		return self._return

class Accords_player(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.fs_violin = fluidsynth.Synth()
		self.fs_violin.start('alsa')
		self.sfid_violin = self.fs_violin.sfload("/home/seevoid/sf2_bank_1/JR__pad.SF2")
		self.fs_violin.program_select(0, self.sfid_violin, 0, 0)

	def run(self):
		while(True):
			self.fs_violin.noteon(0, 60, VOLUME_ACCORDS)
			self.fs_violin.noteon(0, 67, VOLUME_ACCORDS)
			self.fs_violin.noteon(0, 72, VOLUME_ACCORDS)
			time.sleep(12)

			self.fs_violin.noteoff(0, 60)
			self.fs_violin.noteoff(0, 67)
			self.fs_violin.noteoff(0, 72)

			self.fs_violin.noteon(0, 60, VOLUME_ACCORDS)
			self.fs_violin.noteon(0, 66, VOLUME_ACCORDS)
			self.fs_violin.noteon(0, 70, VOLUME_ACCORDS)
			time.sleep(6)

			self.fs_violin.noteoff(0, 60)
			self.fs_violin.noteoff(0, 66)
			self.fs_violin.noteoff(0, 70)

			self.fs_violin.noteon(0, 65, VOLUME_ACCORDS)
			self.fs_violin.noteon(0, 70, VOLUME_ACCORDS)
			self.fs_violin.noteon(0, 75, VOLUME_ACCORDS)
			time.sleep(6)

			self.fs_violin.noteoff(0, 65)
			self.fs_violin.noteoff(0, 70)
			self.fs_violin.noteoff(0, 75)


class Plant(Thread):
	def __init__(self, channel_number, bank_name, synth_name, max_volt, min_volt, max_note, min_note, gamme_active, volume):
		Thread.__init__(self)
		print("YEAH")
		self.stop = False
		self.last_mesure = 0
		self.pot = MCP3008(channel_number)
		self.channel_number = channel_number
		self.max_volt = max_volt
		self.min_volt = min_volt
		self.max_note = max_note
		self.min_note = min_note
		print("CAPTE self.max_volt : ", self.max_volt )
		print("CAPTE self.min_volt : ", self.min_volt )
		self.coeff = (self.max_note - self.min_note) / (self.max_volt - self.min_volt)
		self.gamme_active = gamme_active
		self.volume = volume

		# init fluidsynth
		self.fs = fluidsynth.Synth()
		self.fs.start('alsa')
		self.sfid = self.fs.sfload("/home/seevoid/" + bank_name + "/" + synth_name)
		self.fs.program_select(0, self.sfid, 0, 0)

		self.list_previous_mesure = []
		self.round_nb = 0

	def get_voltage(self):
		# random.seed(random.randrange(1, 6000))
		mesure = NULL_VALUE_VOLT

		good_mesure = False

		while mesure == NULL_VALUE_VOLT:
			mesure = self.pot.value
		
		while not good_mesure:
			mesure = int(self.pot.value*1000)
			if self.round_nb < 1:
				self.list_previous_mesure.append(mesure)
				good_mesure = True
			else:
				if (mesure > self.list_previous_mesure[0] - 1) and (mesure < self.list_previous_mesure[0] + 1) :
					 good_mesure = True
				self.list_previous_mesure[self.round_nb%1] = mesure
			# print("list_previous_mesure : ", self.list_previous_mesure)
			self.round_nb += 1
			time.sleep(0.04)

		# time.sleep(random.randrange(1,100)/100)

		print("mesure: ", mesure)

		if mesure < self.min_volt:
			mesure = self.min_volt
		if mesure > self.max_volt:
			mesure = self.max_volt

		

		return mesure


	def run(self):
		# note_to_play = int((self.volt - self.min_volt)*self.coeff + self.min_note)
		# self.fs.noteon(0, note_to_play, self.volume)
		while (not self.stop):
			good_note = False
			while (not good_note):
				self.volt = self.get_voltage()
				# note_to_play = int(48 + int((self.volt - 48)/(0.33)))
				# self.fs.noteoff(0, note_to_play)
				try:
					self.fs.noteoff(0, note_to_play)
				except:
					print("dommmage")
				note_to_play = int((self.volt - self.min_volt)*self.coeff + self.min_note)
				if (self.gamme_active):
					if (note_to_play%12 in CHOOSEN_GAMME):
						good_note = True
						# print("note_to_play : ", note_to_play)
						self.fs.noteon(0, note_to_play, self.volume)
					else:
						buf = int(note_to_play/12)
						note_to_play = take_closest(CHOOSEN_GAMME, note_to_play%12) + (buf*12)
						# print("note_to_play : ", note_to_play)
						self.fs.noteon(0, note_to_play, self.volume)
				else:
					self.fs.noteon(0, note_to_play, self.volume)
					good_note = True

		

class Timer_calibrage(Thread):
	def __init__(self, seconds):
		Thread.__init__(self)
		self.seconds = seconds
		self.finish = False

	def run(self):
		time.sleep(self.seconds)
		self.finish = True
		print("TIMER DONE")
		time.sleep(5)


def calibrage(timer, channel_number):

	values = []
	timer.start()

	while timer.finish == False:
		val = MCP3008(channel_number).value
		values.append(val)
		# print("value timer : ", timer.finish)
		time.sleep(0.1)

	print("HEY1")
	# print("values : ", values)
	mini = int(min(values) * 1000) - 15
	maxi = int(max(values) * 1000) + 15


	return (mini, maxi)



if __name__ == "__main__":
	# execute only if run as a script

	timer = Timer_calibrage(20)
	

	# accords = Accords_player()
	# accords.start()
 	# plant_1 = Plant(1, "sf2_bank_1", "JR_PADstring.sf2", 90, 5, 96, 24, True, 127)
	# plant_1.start()
	# plant_2 = Plant(2, "sf2_bank_2", "exotic_harp.sf2", 10, 1, 60, 48, True, 127)
	# plant_2.start()

	
	mini_volt, maxi_volt = calibrage(timer, 0)

	print("mini volt : ", mini_volt)
	print("maxi_volt : ", maxi_volt)
	# plant_2 = Plant(0, "sf2_bank_2", "141-compleet_bank__synth.sf2", 20, 0, 108, 48, True, 80)
	plant_2 = Plant(0, "sf2_bank_2", "132-pinkullo2.sf2", maxi_volt, mini_volt,96, 36, True, 95)

	plant_2.start()