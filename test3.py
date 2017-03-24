from colorcycletemplate import ColorCycleTemplate
numLEDs = 144

class StrandTest(ColorCycleTemplate):

    def init(self, strip, numLEDs):
        self.color1 = (255, 0, 0)
        self.color2 = (0, 0, 0)
    def update(self, strip, numLEDs, numStepsPerCycle, currentLED, currentCycle):
        # One cycle = The 9 Test-LEDs wander through numStepsPerCycle LEDs.
        head = currentLED # The head pixel that will be turned on in this cycle
        tail = currentLED # The tail pixel that will be turned off
        if currentCycle == 1:
            for i in range(numLEDs):
                strip.setPixel(i , *self.color1)
        else:
            for i in range(10*(currentCycle-2), 10*(currentCycle - 1)):
                strip.setPixel(i, *self.color2)
        return 1 # Repaint is necessary

a = StrandTest(pauseValue=(0), numStepsPerCycle = numLEDs, numCycles = 15, globalBrightness=5)
a.start()
