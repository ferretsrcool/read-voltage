import time
 
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess
 
# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
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
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype('gargi.ttf', 8)
 
 
# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)
# Write two lines of text.
draw.text((0, top), "Updating Device",  font=font, fill=255)
# Display image.
disp.image(image)
disp.display()
 
from request import request
from json import loads
from subprocess import call
 
files_data = loads(request("http://localhost:8080/file/", "GET")[1])
files_count = len(files_data)
for i in range(files_count):
  draw.rectangle((0,0,width,height), outline=0, fill=0)
  draw.text((0, top), "Updating Device",  font=font, fill=255)
  draw.text((0, top+15)), (" -Updating" + files_data[i]["fileName"]),  font=font, fill=255)
  time.sleep(.2)
  disp.image(image)
  disp.display()
  file = open('src/' + files_data[i]["fileName"], 'w')
  file.write(files_data[i]["fileData"])
  file.close()
 
call('python src/main.py', shell=True)
