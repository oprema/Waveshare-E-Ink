from PIL import Image
import spidev as SPI
from includes.epd import Epd
from includes.icon import Icon
from includes.text import Text
import os, time

WHITE = 1
BLACK = 0
DISPLAY_TYPE = 'EPD_2X9'

def main():
  bus = 0
  device = 0

  spi = SPI.SpiDev(bus, device)
  display = Epd(spi, DISPLAY_TYPE)

  print()
  print("Please consider a donation if you like the software!")
  print("----------------------------------------------------")
  print("Bitcoin: 18U7Ci1wSuMXDJbgkKJwVLK9cs52ZtzL16")
  print("Ether:   0x0F24D31a3a632F4205CBe8025cc13e86ff80a48e")
  print("or Iota: KYDFCQTDJCTLBIJWNT9UIXCN9SXHHSVCT9WDCIZWERJMCPDNZLWVIKOMYSGUVJLRE9CACQPOMZROSARBWYWPPXHHRX")

  for coin in ['btc', 'eth']:
    display.clearDisplayPart()

    # display width and height
    height, width = display.size

    # canvas to draw to
    image = Image.new('1', display.size, WHITE)

    icon_file = "./images/qrcode-%s.png" % coin
    if coin == 'btc':
      xstart, ystart = 14, 14
    else:
      xstart, ystart = 0, 0
    icon = Icon(image, os.path.join(icon_file), xstart=xstart, ystart=ystart)

    # add text beside the icon
    text = Text(width-128, height, ("Consider a donation in %s" % coin))
    image.paste(text.image, (0, 128, 128, 296), mask=BLACK)

    # send image to display
    display.showImageFull(display.imageToPixelArray(image))

    time.sleep(6)

  print("Thank you!")

# main
if "__main__" == __name__:
  main()
