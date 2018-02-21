from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

WHITE = 1
BLACK = 0

class Icon(object):
  def __init__(self, image, icon_file, xstart=14, ystart=14):
    icon = Image.open(icon_file).convert('RGBA')
    icon = icon.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_90)

    self._name = icon_file
    self._image = image
    self._width, self._height = icon.size
    self._image.paste(icon, (xstart, ystart, xstart+self._width, ystart+self._height), mask=icon)

  @property
  def width(self):
    return self._width

  @property
  def height(self):
    return self._height

  @property
  def name(self):
    return self._name
