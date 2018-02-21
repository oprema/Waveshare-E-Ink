#!/usr/bin/python3
import os, sys, subprocess, curses, socket, fcntl, struct
from curses import wrapper

from PIL import Image
from includes.epd import Epd
from includes.text import Text
import spidev as SPI

DISPLAY_TYPE = 'EPD_2X9'
WHITE = 1
BLACK = 0

def sysInfo(eth0info, wlan0info):
  bus, device = 0, 0
  spi = SPI.SpiDev(bus, device)

  display = Epd(spi, DISPLAY_TYPE)
  display.clearDisplayPart()
  height, width = display.size

  # canvas to draw to
  image = Image.new('1', display.size, WHITE)

  # add some text to it
  info = eth0info + wlan0info
  text = Text(width, height, info, chars=24)
  image.paste(text.image, (0, 0, height, width), mask=BLACK)

  # send image to display
  display.showImageFull(display.imageToPixelArray(image))


def getIPAddress(ifname):
  # Return the IP address of interface
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915,  struct.pack('256s', ifname[:15].encode('utf-8')))[20:24])
  except:
    ip = "0.0.0.0"
  return ip

def getMAC(interface):
  # Return the MAC address of interface
  try:
    mac = open('/sys/class/net/' + interface + '/address').read()
  except:
    mac = "00:00:00:00:00:00"
  return mac[0:17]

#
# Main display using curses
#
def main(stdscr):
    # Clear screen and hide cursor
    stdscr.clear()
    curses.curs_set(0)

    # Get system infos
    macEth0, macWlan0 = getMAC('eth0'), getMAC('wlan0')
    ipEth0, ipWlan0 = getIPAddress('eth0'), getIPAddress('wlan0')

    # Add title and footer
    exittxt = 'Press "q" to exit'
    title = '**** System Info ****'
    stdscr.addstr(0, int((curses.COLS - len(title)) / 2), title)
    stdscr.addstr(22, int((curses.COLS - len(exittxt)) / 2), exittxt)
    stdscr.refresh()

    netwin = curses.newwin(4, curses.COLS - 6, 12, 3)
    netwin.erase()
    netwin.border()
    eth0info  = "eth0  IP: %s - MAC: %s" % (ipEth0, macEth0)
    wlan0info = 'wlan0 IP: %s - MAC: %s' % (ipWlan0, macWlan0)
    netwin.addstr(1, 2, eth0info)
    netwin.addstr(2, 2, wlan0info)
    netwin.refresh()

    eth0info  = "- eth0\nIP: %s\nMAC: %s\n" % (ipEth0, macEth0)
    wlan0info = '- wlan0\nIP: %s\nMAC: %s' % (ipWlan0, macWlan0)
    sysInfo(eth0info, wlan0info)

    c = stdscr.getch()
    if c == ord('q'):
        exit();

wrapper(main)

# main
if "__main__" == __name__:
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.exit('interrupted')
