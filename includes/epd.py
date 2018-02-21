import spidev
import RPi.GPIO as GPIO
import time, pprint
import includes.font as font
from PIL import Image

# Global variables
gdo_control = [] # setup in constructor
soft_start  = [0x0c, 0xd7, 0xd6, 0x9d]
vcom_vol    = [0x2c, 0xa8] # VCOM 7c
dummy_line  = [0x3a, 0x1a] # 4 dummy line per gate
gate_time   = [0x3b, 0x08] # 2us per line
ram_data_entry_mode = [0x11, 0x01] # Ram data entry mode
wbuffer = [0 for i in range(5000)]
pp = pprint.PrettyPrinter(indent=4)

# Pin definitions
RST = 17
DC = 25
BUSY = 24
CS = 8

class Epd(object):
  def __init__(self, spi, display):
    if display == "EPD_2X9":
      self._xDot = 128
      self._yDot = 296
      self._delay = 1.5
      self._LUTfull = [
        0x32, 0x02, 0x02, 0x01, 0x11, 0x12, 0x12, 0x22, 0x22,
        0x66, 0x69, 0x69, 0x59, 0x58, 0x99, 0x99, 0x88, 0x00,
        0x00, 0x00, 0x00, 0xF8, 0xB4, 0x13, 0x51, 0x35, 0x51,
        0x51, 0x19, 0x01, 0x00]
      self._LUTpart = [
        0x32, 0x10, 0x18, 0x18, 0x08, 0x18, 0x18, 0x08, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x13, 0x14, 0x44, 0x12, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00]
    elif display == "EPD_2X13":
      self._xDot = 122
      self._yDot = 250
      self._delay = 4.0
      self._LUTfull = [
        0x32, 0x22, 0x55, 0xAA, 0x55, 0xAA, 0x55, 0xAA, 0x11,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1E,
        0x1E, 0x1E, 0x1E, 0x1E, 0x1E, 0x1E, 0x1E, 0x01, 0x00,
        0x00, 0x00, 0x00]
      self._LUTpart = [
        0x32, 0x18, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0F,
        0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00]
    elif display == "EPD_1X54":
      self._xDot = 200
      self._yDot = 200
      self._delay = 1.5
      self._LUTfull = [
        0x32, 0x02, 0x02, 0x01, 0x11, 0x12, 0x12, 0x22, 0x22,
        0x66, 0x69, 0x69, 0x59, 0x58, 0x99, 0x99, 0x88, 0x00,
        0x00, 0x00, 0x00, 0xF8, 0xB4, 0x13, 0x51, 0x35, 0x51,
        0x51, 0x19, 0x01, 0x00]
      self._LUTpart = [
        0x32, 0x10, 0x18, 0x18, 0x08, 0x18, 0x18, 0x08, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x13, 0x14, 0x44, 0x12, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00]
    else:
      raise "Unknown Waveshare Display"

    global gdo_control
    gdo_control = [0x01, (self._yDot-1)%256, int((self._yDot-1)/256), 0x00]

    # Initialize pins
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(RST, GPIO.OUT)
    GPIO.setup(DC, GPIO.OUT)
    GPIO.setup(CS, GPIO.OUT)
    GPIO.setup(BUSY, GPIO.IN)

    # Initialize SPI
    self._spi = spi
    self._spi.max_speed_hz = 2000000
    self._spi.mode = 0b00

  @property
  def xDot(self):
    return self._xDot

  @property
  def yDot(self):
    return self._yDot

  @property
  def size(self):
    return [self._xDot, self._yDot]

  def _readBusy(self):
    for i in range(0, 400):
      if GPIO.input(BUSY) == 0:
        # print 'Busy is Low'
        return
      time.sleep(0.01)

  def _writeCmd(self, command):
    GPIO.output(DC, GPIO.LOW)
    self._spi.writebytes([command])

  def _writeCmdP1(self, command, param):
    self._readBusy()
    GPIO.output(DC, GPIO.LOW)
    self._spi.writebytes([command])
    GPIO.output(DC, GPIO.HIGH)
    self._spi.writebytes([param])

  def _powerOn(self):
    self._writeCmdP1(0x22, 0xc0)
    self._writeCmd(0x20)

  def _write(self, value):
    # Send command byte to display
    GPIO.output(DC, GPIO.LOW)
    time.sleep(0.01)

    # The first byte is written with the command value
    self._spi.writebytes([value[0]])

    GPIO.output(DC, GPIO.HIGH)
    self._spi.writebytes(value[1:])

  def _writeDisplayRam(self, xsize, ysize, data):
    if xsize % 8 != 0:
      xsize = xsize + (8 - xsize % 8)
    xsize /= 8

    self._readBusy()
    GPIO.output(DC, GPIO.LOW)
    self._spi.writebytes([0x24])
    GPIO.output(DC, GPIO.HIGH)

    size = int(xsize * ysize)
    if not isinstance(data, list):
      data = [data] * size

    # SPI buffer size default: 4096 bytes
    i = 0
    for i in range(0, int(size/4096)):
      self._spi.writebytes(data[i:i+4096])
      i += 4096
    self._spi.writebytes(data[i:size])

  def _setRamArea(self, xstart, xend, ystart, ystart1, yend, yend1):
    self._write([0x44, xstart, xend])
    self._write([0x45, ystart, ystart1, yend, yend1])

  def _setRamPointer(self, addrx, addry, addry1):
    self._write([0x4e, addrx])
    self._write([0x4f, addry, addry1])

  def _partDisplay(self, xstart, xend, ystart, ystart1, yend, yend1):
    self._setRamArea(xstart, xend, ystart, ystart1, yend, yend1)
    self._setRamPointer(xstart, ystart, ystart1)

  def _init(self):
    # Initialize display
    # Reset driver
    GPIO.output(CS, GPIO.LOW)
    GPIO.output(RST, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(RST, GPIO.LOW)
    time.sleep(0.01)
    GPIO.output(RST, GPIO.HIGH)

    # Set register
    self._write(gdo_control)  # Pannel configuration, Gate selection
    self._write(soft_start)   # X decrease, Y decrease
    self._write(vcom_vol)     # VCOM setting
    self._write(dummy_line)   # dummy line per gate
    self._write(gate_time)    # Gage time setting
    self._write(ram_data_entry_mode)  # X increase, Y decrease

    # X-source area, Y-gage area
    xdot = self._xDot-1
    ydot = self._yDot-1
    self._setRamArea(0x00, int(xdot/8), ydot%256, int(ydot/256), 0x00, 0x00)
    self._setRamPointer(0x00, ydot%256, int(ydot/256)) # set ram

  def _update(self):
    self._writeCmdP1(0x22, 0xc7)
    self._writeCmd(0x20)
    self._writeCmd(0xff)

  def _updatePart(self):
    self._writeCmdP1(0x22, 0x04)
    self._writeCmd(0x20)
    self._writeCmd(0xff)

  def _initFull(self):
    self._init()
    self._write(self._LUTfull)
    self._powerOn()

  def _initPart(self):
    self._init()
    self._write(self._LUTpart)
    self._powerOn()

  def _displayFull(self, buffer):
    self._setRamPointer(0x00, (self._yDot-1)%256, int((self._yDot-1)/256))
    self._writeDisplayRam(self._xDot, self._yDot, buffer)
    self._update()

  def _displayPart(self, xstart, xend, ystart, yend, buffer):
    self._partDisplay(int(xstart/8), int(xend/8), yend%256, int(yend/256), ystart%256, int(ystart/256))
    self._writeDisplayRam(xend-xstart, yend-ystart+1, buffer)
    self._updatePart()
    time.sleep(0.5)
    self._partDisplay(int(xstart/8), int(xend/8), yend%256, int(yend/256), ystart%256, int(ystart/256))
    self._writeDisplayRam(xend-xstart, yend-ystart+1, buffer)

  # Public methods start here
  #
  def clearDisplayFull(self):
    # Init display
    self._initFull()
    time.sleep(self._delay)

    # Clear screen
    self._displayFull(0xff)
    time.sleep(self._delay)

  def clearDisplayPart(self):
    # Init part of the display
    self._initPart()
    time.sleep(self._delay)

    # Clear screen
    self._displayPart(0, self._xDot-1, 0, self._yDot-1, 0xff)
    time.sleep(self._delay)

  def showImageFull(self, buffer):
    self._displayFull(buffer)

  def showImagePart(self, xstart, xend, ystart, yend, buffer):
    self._displayPart(xstart, xend, ystart, yend, buffer)

  """
  function : Select the character size
  parameters :
    acsii : char data
    size : char len
    mode : char mode
    next : char len
  Remarks:
  """
  def showChar(self, acsii, size, next):
    ch = ord(acsii) - 32

    if size == 12:
      temp = [0 for i in range(11)]
      temp = font.font1206[ch]
    else:
      temp = [0 for i in range(15)]
      temp = font.font1608[ch]

    for i in range(0, size):
      j = size * next + i
      del wbuffer[j]
      wbuffer.insert(j, ~temp[i] & 0xff)

  """
  function : write string
  parameter :
    x : x start address
    y : y start address
    pString : Display data
    Size : char len
  Remarks:
  """
  def showString(self, x, y, str, font):
    strlen = 0
    xaddr = x
    yaddr = y

    if font == "Font16":
      size = 16
    else:
      size = 12

    # 1. Remove the character and determine the character size
    while strlen < len(str):
      if x > self._xDot - size/2:
        x = 0
        y = y + size
        if y > self._yDot - size:
          y = x = 0
      newstr =  str[strlen:strlen+1]
      self.showChar(newstr, size, strlen)
      x = x + size/2
      strlen += 1 # Calculate the current number for the first few characters

    # 2. Show buffer
    self._displayPart(yaddr+1, yaddr+size/2,
      self._yDot-(size*strlen)-xaddr+1, self._yDot-xaddr, wbuffer)

  """
  funtion : Show Image
  parameters :
    xstart : x start address
    ystart : y start address
    buffer : Display data
    xsize : Displays the x length of the image
    ysize : Displays the y length of the image
  Remarks:
    The sample image is 32 * 32
  """
  def showImage(self, xstart, ystart, buffer, xsize, ysize):
    xaddr = int(xstart) * 8
    yaddr = int(ystart) * 8
    self._displayPart(yaddr, yaddr+xsize-1, self._yDot-ysize-xaddr,
      self._yDot-xaddr-1, buffer)

  """
  funtion : Conver PIL image to byte array
  parameters :
    PIL image
  """
  def imageToPixelArray(self, image):
    pixary = ['0' if x==0 else '1' for x in list(image.getdata())]
    v = int(''.join(pixary), 2)
    b = bytearray()
    while v:
      b.append(v & 0xff)
      v >>= 8
    return list(b[::-1])


