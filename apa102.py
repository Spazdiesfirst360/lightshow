import spidev

"""
Driver for APA102 LEDS (aka "DotStar").
(c) Martin Erzberger 2016

My very first Python code, so I am sure there is a lot to be optimized ;)

Public methods are:
 - setPixel
 - setPixelRGB
 - show
 - clearStrip
 - cleanup

Helper methods for color manipulation are:
 - combineColor
 - wheel

"""

rgb_map = { 
    'rgb': [3,2,1], 
    'rbg': [3,1,2], 
    'grb': [2,3,1], 
    'gbr': [2,1,3], 
    'brg': [1,3,2], 
    'bgr': [1,2,3],
}

class APA102:
    def __init__(self, numLEDs, globalBrightness = 31, order='rgb'): 
        self.numLEDs = numLEDs
        order = order.lower()
        self.rgb = rgb_map.get(order, rgb_map['rgb'])
        # LED startframe is three "1" bits, followed by 5 brightness bits
        self.ledstart = (globalBrightness & 0b00011111) | 0b11100000 
        self.leds = [self.ledstart,0,0,0] * self.numLEDs # Pixel buffer
        self.spi = spidev.SpiDev()  
        self.spi.open(0, 1)  # Open SPI port 0, slave device (CS)  1
	# max speed 8000000 causes leds to misbehave
        self.spi.max_speed_hz=800000 

    def clockStartFrame(self):
        """
        void clockStartFrame()
        This method clocks out a start frame, telling the receiving LED 
        that it must update its own color now.
        """
        self.spi.xfer2([0]*4)  # Start frame, 32 zero bits

    def clockEndFrame(self):
        """
        void clockEndFrame()
        """
        for _ in range((self.numLEDs + 15) // 16):  
            self.spi.xfer2([0x00])

    def clearStrip(self):
        """
        void clearStrip()
        Sets the color for the entire strip to black, and immediately 
        shows the result.
        """
        # Clear the buffer
        for led in range(self.numLEDs):
            self.setPixel(led, 0, 0, 0)
        self.show()

    def setPixel(self, ledNum, red, green, blue):
        """
        void setPixel(ledNum, red, green, blue)
        Sets the color of one pixel in the LED stripe. 
        The changed pixel is not shown yet on the Stripe, it is only
        written to the pixel buffer. Colors are passed individually.
        """
        if not (0 <= ledNum < self.numLEDs):
            return # Pixel is invisible, so ignore
        startIndex = 4 * ledNum
        self.leds[startIndex] = self.ledstart
        self.leds[startIndex+self.rgb[0]] = red
        self.leds[startIndex+self.rgb[1]] = green
        self.leds[startIndex+self.rgb[2]] = blue

    def setPixelRGB(self, ledNum, rgbColor):
        """
        void setPixelRGB(ledNum,rgbColor)
        Sets the color of one pixel in the LED stripe. 
        The changed pixel is not shown yet on the Stripe, it is only
        written to the pixel buffer. Colors are passed combined 
        (3 bytes concatenated)
        """
        self.setPixel(ledNum, 
                (rgbColor & 0xFF0000) >> 16, 
                (rgbColor & 0x00FF00) >> 8, 
                rgbColor & 0x0000FF)

    def rotate(self, positions=1):
        """
        void rotate(positions)
        Treating the internal leds array as a circular buffer, 
        rotate it by the specified number of positions.
        The number could be negative, which means rotating in the 
        opposite direction.
        """
        cutoff = 4 * (positions % self.numLEDs)
        self.leds = self.leds[cutoff:] + self.leds[:cutoff]

    def show(self):
        """
        void show()
        Sends the content of the pixel buffer to the strip.
        Todo: More than 1024 LEDs requires more than one xfer operation.
        """
        self.clockStartFrame()
        # xfer2 kills the list, unfortunately. So it must be copied first
        self.spi.xfer2(list(self.leds)) # SPI takes up to 4096 Integers. So we are fine for up to 1024 LEDs.
        self.clockEndFrame()

    def cleanup(self):
        """
        void cleanup()
        This method should be called at the end of a program in order to 
        release the SPI device
        """
        self.spi.close()  # ... SPI Port schliessen

    def combineColor(self, red, green, blue):
        """
        color combineColor(red,green,blue)
        Make one 3*8 byte color value
        """
        return (red << 16) + (green << 8) + blue

    def wheel(self, wheelPos):
        """
        color wheel(wheelPos)
        Get a color from a color wheel
        Green -> Red -> Blue -> Green
        """
        if wheelPos > 255: wheelPos = 255 # Safeguard
        if wheelPos < 85: # Green -> Red
            return self.combineColor(wheelPos * 3, 255 - wheelPos * 3, 0)
        elif wheelPos < 170: # Red -> Blue
            wheelPos -= 85
            return self.combineColor(255 - wheelPos * 3, 0, wheelPos * 3)
        else: # Blue -> Green
            wheelPos -= 170
            return self.combineColor(0, wheelPos * 3, 255 - wheelPos * 3);

    def dumparray(self):
        """
        void dumparray()
        For debug purposes: Dump the LED array onto the console.
        """
        print(self.leds)
