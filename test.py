from colorcycletemplate import ColorCycleTemplate
numLEDs = 144

class StrandTest(ColorCycleTemplate):

    def init(self, strip, numLEDs):
        self.color1 = (135, 206, 250)
        self.color2 = (255, 45, 0)
    def update(self, strip, numLEDs, numStepsPerCycle, currentLED, currentCycle):
        # One cycle = The 9 Test-LEDs wander through numStepsPerCycle LEDs.
        head = (currentLED + 9) % numStepsPerCycle # The head pixel that will be turned on in this cycle
        tail = currentLED # The tail pixel that will be turned off
        if currentCycle % 2 == 1:
            strip.setPixel(head, *self.color1)
        else:
            strip.setPixel(head, *self.color2)  # Paint head
        strip.setPixelRGB(tail, 0)  # Clear tail

        return 1 # Repaint is necessary

a = StrandTest(pauseValue=0, numStepsPerCycle = numLEDs, numCycles = 6, globalBrightness=10)
a.start()
