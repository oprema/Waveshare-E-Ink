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

ICON_SIZE = 100

def main():
  bus = 0
  device = 0

  spi = SPI.SpiDev(bus, device)
  display = Epd(spi, DISPLAY_TYPE)

  # initially set all white background
  image = Image.new('1', display.size, WHITE)
  icon_mask = Image.new('1', (ICON_SIZE, ICON_SIZE), WHITE)

  # prepare for drawing a text
  draw = ImageDraw.Draw(image)
  font = ImageFont.truetype(FONT_FILE, FONT_SIZE)

  print('--> Init and clear full screen')
  display.clearDisplayPart()
  #display.clearDisplayFull()

  while True:
    for file in os.listdir("./png-icons/%d/" % ICON_SIZE):
      if file.endswith(".png"):

        image = Image.new('1', display.size, WHITE)
        icon_file = os.path.join(("./png-icons/%d/" % ICON_SIZE), file)

        icon = Image.open(icon_file).convert('RGBA')
        icon = icon.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_90)

        width, height = icon.size
        xstart, ystart = 14, 14
        image.paste(icon, (xstart, ystart, xstart+width, ystart+height), mask=icon)
        print("--> Prepare PNG: %s (size: %d x %d)" % (icon_file, width, height))

        text = Image.new('1', (128, 128), WHITE)
        width, height = text.size
        font = ImageFont.truetype(FONT_FILE, FONT_SIZE)

        draw = ImageDraw.Draw(text)
        draw.text((4, 4), "ABCDEFGHIJKLMNOP", fill=BLACK, font=font)
        #text = text.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_90)
        #draw.rectangle(((1, 1), (50, 100)), fill=BLACK)
        image.paste(text, (0, 0, 128, 128), mask=text)
        print("--> Prepare text: size: %d x %d" % (width, height))

        # send image to display
        display.showImageFull(display.imageToPixelArray(image))

        time.sleep(2)
        display.clearDisplayPart()

# main
if "__main__" == __name__:
  main()
