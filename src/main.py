"""Main file containing running loop of program."""
from RPi import GPIO  # noqa: I003

import os  # noqa: I001
import read_file as rf  # noqa: I001
import time  # noqa: I001
import smbus  # noqa: I001
import httplib2

i2c_ch = 1
adc_add = 0x68
bus = smbus.SMBus(i2c_ch)
con = 24
bus.write_byte(adc_add, con)

# pin setup
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Power , GPIO-18
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Start/Stop , GPIO - 23
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Real time/ Average , GPIO - 25


def request(url, method):
    """HTTP request function."""
    h = httplib2.Http(".cache")
    return h.request(url, method)

# button interupt functions
def power_callback(channel):
    """Shut down interupt."""
    print("Power Off")
    request(config.API_URL + "/reading", "POST")
    os.system("shutdown now -h")


def start_callback(channel):
    """Start/Stop reading interupt."""
    global start
    start = not start
    if (not start):
        request(config.API_URL + "/reading", "POST")
        print("STOP READING")
    else:
        print("START READING")


def mode_callback(channel):
    """Average reading/Continuous reading modes interupt."""
    global real_time
    real_time = not real_time
    if (not real_time):
        print("AVERAGE READINGS")
    else:
        print("REAL TIME READINGS")


def av_list(list):
    """Get average of last 3 readings."""
    length = len(list)
    tot = 0
    for i in range(0, length):
        tot = tot + list[i]
    av = tot / length
    return av


# button interupt setup
GPIO.add_event_detect(12, GPIO.FALLING, callback=power_callback, bouncetime=500)
GPIO.add_event_detect(16, GPIO.FALLING, callback=start_callback, bouncetime=500)
GPIO.add_event_detect(22, GPIO.FALLING, callback=mode_callback, bouncetime=500)

# initial values
start = False
real_time = True
mag = rf.get_sample()
mag_list = [mag]
val = 0

# main loop
while(1):
    if(start):                     # only starts reading in start mode
        mag = rf.get_sample()       # reads sample
        request(config.API_URL + "/reading/" + str(mag), "POST")
        mag_list.append(mag)        # adds to a list of the previous 10 values

        # deletes the first value if there are more than 10 in the list
        if(len(mag_list) > 10):
            del mag_list[0]
        # if in real time mode print value is just the last reading
        if (real_time):
            val = mag
        # if in average mode print value is the average of the list
        else:
            val = av_list(mag_list)
        print(val)                  # prints the print value
    time.sleep(.3)
