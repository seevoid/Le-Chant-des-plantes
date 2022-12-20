from gpiozero import MCP3008
import time
import sys
from gpiozero.tools import smoothed
pot = MCP3008(int(sys.argv[1]))

while True:
	print("value : ", pot.value/0.076)
	# print(smoothed(pot.value, 5))
	# for value in smoothed(pot.values, 5):
	# 	print(value)
		# time.sleep(1)
	time.sleep(0.1)

