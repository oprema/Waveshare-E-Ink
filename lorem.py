from PIL import Image
from includes.epd import Epd
from includes.text import Text

import spidev as SPI
import os, time

WHITE = 1
BLACK = 0
DISPLAY_TYPE = 'EPD_2X9'

def main():
  bus, device = 0, 0
  spi = SPI.SpiDev(bus, device)
  display = Epd(spi, DISPLAY_TYPE)

  print('--> Init and clear full screen %s' % display.size)
  display.clearDisplayPart()

  height, width = display.size

  # canvas to draw to
  image = Image.new('1', display.size, WHITE)

  # add some text to it
  text = Text(width, height, "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.", chars=24)
  image.paste(text.image, (0, 0, height, width), mask=BLACK)

  # send image to display
  display.showImageFull(display.imageToPixelArray(image))

# main
if "__main__" == __name__:
  main()
