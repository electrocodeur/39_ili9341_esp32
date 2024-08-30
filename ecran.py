"""cablage : 

ESP32 GPIO  |  ILI9341
------------|---------------------
3.3V        |  VCC
GND         |  GND
GPIO 16     |  CS (Chip Select)
GPIO 4      |  DC/RS (Data/Command)
GPIO 17     |  RESET
GPIO 13     |  SDI (MOSI)
GPIO 12     |  SDO (MISO)
GPIO 14     |  SCK (Clock)
GPIO 18     |  T_CLK (Touch Clock)
GPIO 5      |  T_CS (Touch Chip Select)
GPIO 23     |  T_DIN (Touch Data In)
GPIO 19     |  T_DO (Touch Data Out)
GPIO 21     |  T_IRQ (Touch Interrupt)
"""

from ili9341 import Display, color565
from xpt2046 import Touch
from machine import idle, Pin, SPI  # type: ignore


class Demo(object):
    """Touchscreen simple demo."""
    CYAN = color565(0, 255, 255)
    PURPLE = color565(255, 0, 255)
    WHITE = color565(255, 255, 255)

    def __init__(self, display, spi2):
        """Initialize box.

        Args:
            display (ILI9341): display object
            spi2 (SPI): SPI bus
        """
        self.display = display
        self.touch = Touch(spi2, cs=Pin(5), int_pin=Pin(21),
                           int_handler=self.touchscreen_press)
        # Display initial message
        self.display.draw_text8x8(self.display.width // 2 - 32,
                                  self.display.height - 9,
                                  "TOUCH ME",
                                  self.WHITE,
                                  background=self.PURPLE)

        # A small 5x5 sprite for the dot
        self.dot = bytearray(b'\x00\x00\x07\xE0\xF8\x00\x07\xE0\x00\x00\x07\xE0\xF8\x00\xF8\x00\xF8\x00\x07\xE0\xF8\x00\xF8\x00\xF8\x00\xF8\x00\xF8\x00\x07\xE0\xF8\x00\xF8\x00\xF8\x00\x07\xE0\x00\x00\x07\xE0\xF8\x00\x07\xE0\x00\x00')

    def touchscreen_press(self, x, y):
        """Process touchscreen press events."""
        # Y needs to be flipped
        #y = (self.display.height - 1) - y
        # Display coordinates
        self.display.draw_text8x8(self.display.width // 2 - 32,
                                  self.display.height - 9,
                                  "{0:03d}, {1:03d}".format(x, y),
                                  self.CYAN)
        # Draw dot
        self.display.draw_sprite(self.dot, x - 2, y - 2, 5, 5)
        print("X : ",x,", Y :",y)
        if x > 180 and x < 240 and y > 0 and y < 60:
            print("Vous appuyez sur le bouton")

def test():
    """Test code."""
    #spi1 = SPI(1, baudrate=40000000, sck=Pin(14), mosi=Pin(13))
    spi1 = SPI(1, baudrate=40000000, polarity=1, phase=1, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
    display = Display(spi1, dc=Pin(4), cs=Pin(16), rst=Pin(17), rotation=0)
    spi2 = SPI(2, baudrate=1000000, sck=Pin(18), mosi=Pin(23), miso=Pin(19))

    Demo(display, spi2)
    try:
        while True:
            idle()

    except KeyboardInterrupt:
        print("\nCtrl-C pressed.  Cleaning up and exiting...")
    finally:
        display.cleanup()


test()

