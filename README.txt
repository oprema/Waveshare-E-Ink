sudo apt-get install python3-pip libtiff5-dev libopenjp2-7-dev fonts-freefont-ttf 
sudo pip3 install RPi.GPIO spidev qrcode Pillow twython python-dotenv

activate spi in raspi-config

Examples:
python3 hello.py -> Hello world example
python3 main.py -> Same as the original from waveshare
python3 donation.py -> Shows QR-codes for a donation :-)
python3 icons.py -> Font awesome icons
python3 system -> System infos

# Twitter authorisation keys
# please rename .env-example to .env and
# define the keys and secrets to get the twitter client going
python3 twitter -> A twitter client to show news and more
