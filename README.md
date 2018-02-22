# waveshare-e-ink
This is rewrite of Waveshares 2.9 and 1.54 inch e-ink paper display driver
for the Raspberry Pi in python (version 2 and 3). The original source code can be found at:
https://www.waveshare.com/wiki/2.9inch_e-Paper_Module

### Important: Activate the SPI interface through raspi-config

### Wiring Plan: E-Ink-Display <-> Raspi
```
Display   Raspi   
3.3V      3.3V - Pin 17   
GND       GND  - Pin 20   
DIN       MOSI - Pin 19   
CLK       SCLK - Pin 23   
CS        CE0  - Pin 24   
DC        GPIO 25 - Pin 22   
RST       GPIO 17 - Pin 11   
BUSY      GPIO 24 - Pin 18   
```

### Software to install:
```
sudo apt-get install python3-pip libtiff5-dev libopenjp2-7-dev fonts-freefont-ttf
sudo pip3 install RPi.GPIO spidev qrcode Pillow twython python-dotenv
```
#### Examples:
python3 lorem.py -> Lorem Ipsum example   
python3 main.py -> Same as the original from waveshare   
python3 donation.py -> Shows QR-codes for a donation :-)   
python3 icons.py -> Font awesome icons and icon names   
python3 system -> System infos   

> Twitter authorisation keys   
> please rename .env-example to .env and   
> define the keys and secrets to get the twitter client going   

python3 twitter -> A twitter client to show news and more
