#!/usr/bin/python3
# coding: utf-8
# extracted from papirus-twitter

# import libraries to make it work
import os, sys, string, re, time
from twython import Twython
from PIL import Image
from includes.epd import Epd
from includes.text import Text
import spidev as SPI

from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Twitter authorisation keys
# please rename .env-example to .env and
# define the keys and secrets
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
ACCESS_KEY = os.environ.get("ACCESS_KEY")
ACCESS_SECRET = os.environ.get("ACCESS_SECRET")

WHITE = 1
BLACK = 0
DISPLAY_TYPE = 'EPD_2X9'

class Twitter(object):
  def __init__(self):
    self._twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)

  def credentials(self):
    return self._twitter.verify_credentials()

  def getTweets(self, channel):
    tweets = self._twitter.get_user_timeline(screen_name=channel, count=5)
    texts = []
    for tweet in tweets:
      text = '%s: %s' % (tweet['user']['screen_name'], tweet['text'])

      # These lines clear URLs from the tweets and tidies up other elements
      # the waveshare display doesn't seem to like
      text = re.sub(r"(https?\://|http?\://|https?\:)\S+", "", text)
      text = re.sub(r"&amp;", "&", text)
      text = re.sub(r"&horbar|&hyphen|&mdash|&ndash", "-", text)
      text = re.sub(r"&apos|&rsquo|&rsquor|&prime", "", text)
      text = re.sub(r"£|'|\"|\n", "", text)
      text = text.encode("ascii", "ignore").decode('UTF-8')
      texts.append(text)
    return texts


def main():
  t = Twitter()
  bus, device = 0, 0
  spi = SPI.SpiDev(bus, device)
  display = Epd(spi, DISPLAY_TYPE)

  display.clearDisplayPart()
  height, width = display.size

  while True:
    # Put the Twitter usernames of the news organisations you want to read here
    twits = ["SPIEGELONLINE", "SkyNews", "WetterOnline"]

    for twit in twits:
      for tweet in t.getTweets(twit):

        # canvas to draw to
        image = Image.new('1', display.size, WHITE)

        # add some text to it
        print(tweet)
        text = Text(width, height, tweet, chars=24)
        image.paste(text.image, (0, 0, height, width), mask=BLACK)

        # send image to display
        display.showImageFull(display.imageToPixelArray(image))

        # Sets how many seconds each tweet is on screen for
        time.sleep(5)

if __name__ == '__main__':
  main()
