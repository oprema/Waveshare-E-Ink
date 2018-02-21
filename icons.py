from PIL import Image
from includes.epd import Epd
from includes.icon import Icon
from includes.text import Text

import spidev as SPI
import os, time

WHITE = 1
BLACK = 0
DISPLAY_TYPE = 'EPD_2X9'
ICON_SIZE = 100

def main():
  bus, device = 0, 0
  spi = SPI.SpiDev(bus, device)
  display = Epd(spi, DISPLAY_TYPE)

  print('--> Init and clear full screen %s' % display.size)
  display.clearDisplayPart()

  while True:
    for file in os.listdir("./png-icons/%d/" % ICON_SIZE):
      if file.endswith(".png"):
        # display width and height
        height, width = display.size

        # canvas to draw to
        image = Image.new('1', display.size, WHITE)

        # add icon to canvas
        icon = Icon(image, os.path.join(("./png-icons/%d/" % ICON_SIZE), file))
        print("--> Prepare PNG: %s (size: %d x %d)" % (file, icon.width, icon.height))

        # add text beside the icon
        text = Text(width-128, height, file)
        image.paste(text.image, (0, 128, 128, 296), mask=BLACK)

        # send image to display
        display.showImageFull(display.imageToPixelArray(image))

        time.sleep(2)
        display.clearDisplayPart()

# main
if "__main__" == __name__:
  main()
