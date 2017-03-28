from colorcycletemplate import ColorCycleTemplate
numLEDs = 144
class Victory(ColorCycleTemplate):
	def init(self, strip, numLEDs):
		self.color = (0, 255, 0)
		
	def update(self, strip, numLEDs, numStepsPerCycle, currentStep, currentCycle):
		strip.setPixel(53,*self.color)
		return 1

myCycle = Victory(pauseValue=1, numStepsPerCycle = 1, numCycles = 1)
myCycle.start()