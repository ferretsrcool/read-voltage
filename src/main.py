import RPi.GPIO as GPIO
import os
import read_file as rf
import time
import smbus
import requests

i2c_ch = 1
adc_add = 0x68
bus = smbus.SMBus(i2c_ch)
con = 24
bus.write_byte(adc_add, con)

#pin setup
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Power , GPIO-18
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Start/Stop , GPIO - 23
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Real time/ Average , GPIO - 25


#button interupt functions
def power_callback(channel):
    print("Power Off")
    os.system("shutdown now -h")

def start_callback(channel):
    global start
    start = not start
    if (not start):
        #requests.post("http://10.14.176.120:8080/reading")
        print ("STOP READING")
    else:
        print ("START READING")

def mode_callback(channel):
    global real_time
    real_time = not real_time
    if (not real_time):
        print("AVERAGE READINGS")
    else:
        print("REAL TIME READINGS")
def av_list(list):
    l = len(list)
    tot = 0
    for i in range (0, l):
        tot = tot + list[i]
    av = tot/l
    return av

#button interupt setup
GPIO.add_event_detect(12, GPIO.FALLING, callback = power_callback, bouncetime=500)
GPIO.add_event_detect(16, GPIO.FALLING, callback = start_callback, bouncetime=500)
GPIO.add_event_detect(22, GPIO.FALLING, callback = mode_callback, bouncetime=500)



#initial values
start = False
real_time = True
mag = rf.get_sample()
mag_list = [mag]
val = 0

#main loop
while(1):
    if (start):                     #only starts reading in start mode
        mag = rf.get_sample()       #reads sample
        #print(requests.post("http://10.14.176.120:8080/reading/" + str(mag)))
        mag_list.append(mag)        #adds to a list of the previous 10 values
        if (len(mag_list) > 10):    #deletes the first value if there are more than 10 in the list
            del mag_list[0]
        if (real_time):             #if in real time mode print value is just the last reading
            val = mag
        else:                       #if in average mode print value is the average of the list
            val = av_list(mag_list)
        print(val)                  #prints the print value
    time.sleep(.3)
