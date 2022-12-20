import RPi.GPIO as GPIO

import time

GPIO.cleanup()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(21, GPIO.OUT)

GPIO.output(21,True)


time.sleep(10)


GPIO.output(21,False)

print("finish")