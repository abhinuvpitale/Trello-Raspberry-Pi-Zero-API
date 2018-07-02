# Copyright (c) 2017 Adafruit Industries
# Author: Tony DiCola & James DeVito
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import RPi.GPIO as GPIO

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

import trelloParsers as tp

# Get Trello API Keys
f = open('keys.dat')
KEY = str(f.readline()).strip()
TOKEN = str(f.readline()).strip()
BOARD = str(f.readline()).strip()
f.close()

# URL to fetch my boards
url = 'https://api.trello.com/1/boards/'+BOARD+'/lists?cards=open&key='+KEY+'&token='+TOKEN

# Input pins:
L_pin = 27
R_pin = 23
C_pin = 4
U_pin = 17
D_pin = 22

A_pin = 5
B_pin = 6

GPIO.setmode(GPIO.BCM)

GPIO.setup(A_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(B_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(L_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(R_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(U_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(D_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(C_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up

# Raspberry Pi pin configuration:
RST = 24     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
#font = ImageFont.truetype('pixelmix.ttf', 8)
print 'Before Cards'
# Trell Stuff
cards = tp.getCardsFromURL(url)

nCards = len(cards)
dispDepth = 3

currCard = 0
currDepth = 0

maxDepth = len(cards[sorted(cards.keys())[currCard%nCards]])

# Var Inits
u_pin_old = 0
d_pin_old = 0
l_pin_old = 0
r_pin_old = 0
while True:
    # GPIO Poll
    u_pin = GPIO.input(U_pin)
    d_pin = GPIO.input(D_pin)
    l_pin = GPIO.input(L_pin)
    r_pin = GPIO.input(R_pin)

    if l_pin == 1 and l_pin_old == 0:
        currCard = currCard + 1
        currDepth = 0
        maxDepth = len(cards[sorted(cards.keys())[currCard%nCards]])
    if r_pin == 1 and r_pin_old == 0:
        currCard = currCard - 1
        currDepth = 0
        maxDepth = len(cards[sorted(cards.keys())[currCard%nCards]])
    if u_pin == 1 and u_pin_old == 0:
        if currDepth != 0:
            currDepth = currDepth - 1
    if d_pin == 1 and d_pin_old == 0:
        if currDepth != maxDepth - 3:
         currDepth = currDepth + 1

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Write two lines of text.
    currCardName = sorted(cards.keys())[currCard%nCards]
    currList = cards[currCardName]
    try :
        todo0 = str(currList[currDepth + 0])
    except Exception:
        todo0 = ''
    try :
        todo1 = str(currList[currDepth + 1])
    except Exception:
        todo1 = ''
    try :
        todo2 = str(currList[currDepth + 2])
    except Exception:
        todo2 = ''
    draw.text((x, top),       "Card:: "+str(currCardName),  font=font, fill=255)
    draw.text((x, top+8),     ""+todo0, font=font, fill=255)
    draw.text((x, top+16),    ""+todo1,  font=font, fill=255)
    draw.text((x, top+25),    ""+todo2,  font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()
    u_pin_old = u_pin
    d_pin_old = d_pin
    l_pin_old = l_pin
    r_pin_old = r_pin
    time.sleep(.1)
