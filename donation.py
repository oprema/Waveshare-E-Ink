from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import spidev as SPI
from epd import Epd
import os, time

WHITE = 1
BLACK = 0
FONT_FILE = '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf'
FONT_SIZE = 28
DISPLAY_TYPE = 'EPD_2X9'

def main():
  bus = 0
  device = 0

  spi = SPI.SpiDev(bus, device)
  display = Epd(spi, DISPLAY_TYPE)

  print('--> Init and clear full screen')
  display.clearDisplayPart()

  image = Image.new('1', display.size, WHITE)
  icon_file = "./qrcode.png"
  icon = Image.open(icon_file).convert('RGBA')
  icon = icon.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_90)
  print(list(icon.getdata()))
  #print([True if x==0 else False for x in list(icon.getdata())])

  width, height = icon.size
  xstart, ystart = 14, 14
  image.paste(icon, (xstart, ystart, xstart+width, ystart+height), mask=icon)
  print("--> Show PNG: %s (size: %d x %d)" % (icon_file, width, height))

#  draw.text((4, 4), "ABCDEF", fill=BLACK, font=font)
#  draw.rectangle(((1, 1), (50, 100)), fill=BLACK)

  # send image to display
  #pixels = list(image.getdata())
  #pixary = ['0' if x==0 else '1' for x in list(image.getdata())]
  #binstr = ''.join(pixary)
  #print(binstr)
  bytary = display.imageToPixelArray(image)
  print(bytary)
  display.showImageFull(bytary)


# main
if "__main__" == __name__:
  main()
