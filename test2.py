from colorcycletemplate import ColorCycleTemplate
numLEDs = 144

class StrandTest(ColorCycleTemplate):

    def init(self, strip, numLEDs):
        self.color1 = (135, 206, 250)
        self.color2 = (255, 45, 0)
        self.color3 = (0, 0, 0)
    def update(self, strip, numLEDs, numStepsPerCycle, currentLED, currentCycle):
        # One cycle = The 9 Test-LEDs wander through numStepsPerCycle LEDs.
        head = currentLED # The head pixel that will be turned on in this cycle
        tail = currentLED # The tail pixel that will be turned off
        if currentCycle % 4 == 1:
            strip.setPixel(head, *self.color3)
        elif currentCycle % 4 == 2:
            strip.setPixel(head, *self.color1)  # Paint head
        elif currentCycle % 4 == 3:
            strip.setPixel(head, *self.color3)
        else:
            strip.setPixel(head,*self.color2)

        return 1 # Repaint is necessary

a = StrandTest(pauseValue=0.01, numStepsPerCycle = numLEDs, numCycles = 20, globalBrightness=5) #numCycles is even number for this pattern
a.start()
