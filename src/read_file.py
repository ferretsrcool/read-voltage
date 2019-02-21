#import smbus
import time

#adc_add = tbd
#reg = tbd

v_ref = 2.048 #tbd
lsb = 2 * v_ref / (1 << 16) #size of quantisation level
pga = 1 #programmable gain amplifier of adc

gain = 1 #tbd based on amplifier

#reads the i2c input data and returns the adc output code
def read_data():
    #data_read = bus.read_i2c_block_data(adc_add, reg, 2) # (i2c address, register to be stored in, number of bytes to be read)
    data_read = [0x00, 0xFF] #format of the data read above [msbyte, lsbyte]

    temp = (data_read[0] << 8) | data_read[1] #concatinates the bytes of the input data

    val = twos_comp(temp) # converts twos compliment number

    return val

#calculates the input voltage to the adc from the received code
def conv_voltage(val):
    global lsb, pga

    voltage = val*lsb / pga

    return voltage

#calculates the magnetic field from a recorded voltage
def conv_magnetic(voltage):
    global gain

    voltage = voltage/gain

    #tbd conversion of magnetic field to voltage based on probe

    return voltage

# converts twos compliment number
def twos_comp(val):
    if (val & (1 << (15))) != 0:
        val = val - (1 << 16)
    return val

def av_list(list):
    l = len(list)
    tot = 0
    for i in range (0, l):
        tot = tot + list[i]
    av = tot/l
    return av

time.sleep(1) # setup time

#getting the first 10 values
val = read_data()
voltage = conv_voltage(val)
mag = conv_magnetic(voltage)
mag_list = [mag]
for i in range (0,9):
    val = read_data()
    voltage = conv_voltage(val)
    mag = conv_magnetic(voltage)
    mag_list.append(mag)
    time.sleep(0.1)

while(1):
    val = read_data()
    voltage = conv_voltage(val)
    mag = conv_magnetic(voltage)
    mag_list.append(mag)
    del mag_list[0]
    averageM = av_list(mag_list)
    print(averageM)
    time.sleep(0.1)