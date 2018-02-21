from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import textwrap

WHITE = 1
BLACK = 0
FONT_PATH = '/usr/share/fonts/truetype/freefont/'
FONT_DEFAULT = 'FreeMonoBold.ttf'
FONT_SIZE = 20

class Text(object):
  def __init__(self, width, height, text, xtext=6, ytext=6, chars=14, font_file=None):
    image = Image.new('1', (width, height), WHITE)
    if font_file == None:
      font_file = FONT_DEFAULT
    font = ImageFont.truetype(FONT_PATH + font_file, FONT_SIZE)

    draw = ImageDraw.Draw(image)
    w = textwrap.TextWrapper(width=chars, break_long_words=False) #, replace_whitespace=False)
    for line in text.splitlines(): 
      for frag in w.wrap(line):
        #print("Line: '%s'" % frag)
        width, height = font.getsize(frag)
        draw.text((xtext, ytext), frag, font=font, fill=BLACK)
        ytext += height
    self._image = image.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_90)

  @property
  def image(self):
    return self._image

