import random, math
from PIL import Image
import time
from threading import Thread
from threading import Event

PROBABILITY = 0.10

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

random.seed()

class X:
	 def eval(self, x, y):
			return x
	 
	 def __str__(self):
			return "x"

class Y:
	 def eval(self, x, y):
			return y
	 
	 def __str__(self):
			return "y"

class SinPi:
	 def __init__(self, prob, color):
			if (color == 'red'):
				self.arg = buildExprRed(prob * prob)
			if (color == 'green'):
				self.arg = buildExprGreen(prob * prob)
			if (color == 'blue'):
				self.arg = buildExprBlue(prob * prob)
	 
	 def __str__(self):
			return "sin(pi*" + str(self.arg) + ")"

	 def eval(self, x, y):
			return math.sin(math.pi * self.arg.eval(x,y))

class CosPi:
	 def __init__(self, prob, color):
			if (color == 'red'):
				self.arg = buildExprRed(prob * prob)
			if (color == 'green'):
				self.arg = buildExprGreen(prob * prob)
			if (color == 'blue'):
				self.arg = buildExprBlue(prob * prob)

	 def __str__(self):
			return "cos(pi*" + str(self.arg) + ")"

	 def eval(self, x, y):
			return math.cos(math.pi * self.arg.eval(x,y))

class Times:
	 def __init__(self, prob, color):
			if (color == 'red'): 
				self.lhs = buildExprRed(prob * prob)
				self.rhs = buildExprRed(prob * prob)
			if (color == 'green'):
				self.lhs = buildExprGreen(prob * prob)
				self.rhs = buildExprGreen(prob * prob)
			if (color == 'blue'):
				self.lhs = buildExprBlue(prob * prob)
				self.rhs = buildExprBlue(prob * prob)

	 def __str__(self):
			return str(self.lhs) + "*" + str(self.rhs)

	 def eval(self, x, y):
			return self.lhs.eval(x,y) * self.rhs.eval(x,y)

def buildExprRed(prob = 0.99):
	 if random.random() < prob:
			return random.choice([SinPi(prob=prob, color='red'), CosPi(prob=prob, color='red'), Times(prob=prob, color='red')])
	 else:
			return random.choice([X, Y])()

def buildExprGreen(prob = 0.99):
	 if random.random() < prob:
			return random.choice([SinPi(prob=prob, color='green'), CosPi(prob=prob, color='green'), Times(prob=prob, color='green')])
	 else:
			return random.choice([X, Y])()

def buildExprBlue(prob = 0.99):
	 if random.random() < prob:
			return random.choice([SinPi(prob=prob, color='blue'), CosPi(prob=prob, color='blue'), Times(prob=prob, color='blue')])
	 else:
			return random.choice([X, Y])()

def plotIntensity(exp, pixelsPerUnit = 150):
		canvasWidth = 2 * pixelsPerUnit + 1
		canvas = Image.new("L", (canvasWidth, canvasWidth))

		for py in range(canvasWidth):
				for px in range(canvasWidth):
						# Convert pixel location to [-1,1] coordinates
						x = float(px - pixelsPerUnit) / pixelsPerUnit 
						y = -float(py - pixelsPerUnit) / pixelsPerUnit
						z = exp.eval(x,y)

						# Scale [-1,1] result to [0,255].
						intensity = int(z * 127.5 + 127.5)
						canvas.putpixel((px,py), intensity)

		return canvas

def plotColor(redExp, greenExp, blueExp, pixelsPerUnit = 500):
		redPlane   = plotIntensity(redExp, pixelsPerUnit)
		greenPlane = plotIntensity(greenExp, pixelsPerUnit)
		bluePlane  = plotIntensity(blueExp, pixelsPerUnit)
		return Image.merge("RGB", (redPlane, greenPlane, bluePlane))

def makeImage(numPics = 1):
	 # with open("eqns.txt", 'w') as eqnsFile:
		for i in range(numPics):
			 # redExp = buildExpr()
			 redExp = ThreadWithReturnValue(target=buildExprRed, args=(PROBABILITY,))
			 redExp.start()
			 
			 # greenExp = buildExpr()
			 greenExp = ThreadWithReturnValue(target=buildExprGreen, args=(PROBABILITY,))
			 greenExp.start()
			 
			 # blueExp = buildExpr()
			 blueExp = ThreadWithReturnValue(target=buildExprBlue, args=(PROBABILITY,))
			 blueExp.start()
			 

			 redExp = redExp.join()
			 greenExp = greenExp.join()
			 blueExp = blueExp.join()

			 # print("test : ", test)
			 # print("redExp : ", redExp)
			 # print("greenExp : ", greenExp)
			 # print("blueExp : ", blueExp)
			 # time.sleep(3)

			 # eqnsFile.write("img" + str(i) + ":\n")
			 # eqnsFile.write("red = " + str(redExp) + "\n")
			 # eqnsFile.write("green = " + str(greenExp) + "\n")
			 # eqnsFile.write("blue = " + str(blueExp) + "\n\n")

			 image = plotColor(redExp, greenExp, blueExp)
			 image.save("img" + str(i) + ".png", "PNG")

makeImage(50)