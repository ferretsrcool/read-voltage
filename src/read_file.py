
# reads the i2c input data and returns the adc output code
def read_data():

    # adc_add = 0x60 for example, address of the adc on i2c bus
    # reg = 0x01 address for the data from bus to be saved to
    # data_read = bus.read_i2c_block_data(adc_add, reg, 2)
    #             (i2c address, register to be stored in, number of bytes to be read)

    data_read = [0x00, 0xFF] # format of the data read above [msbyte, lsbyte], temporary

    temp = (data_read[0] << 8) | data_read[1] # concatenates the bytes of the input data

    val = twos_comp(temp) # converts twos compliment number

    return val

# calculates the input voltage to the adc from the received code
def conv_voltage(val):

    v_ref = 2.048  # full range of input voltage
    lsb = 2 * v_ref / (1 << 16)  # size of quantisation level
    pga = 1  # programmable gain amplifier of adc

    voltage = val*lsb / pga

    return voltage

# calculates the magnetic field from a recorded voltage
def conv_magnetic(voltage):
    gain = 1 # tbd based on amplifier circuit

    voltage = voltage/gain

    # tbd conversion of magnetic field to voltage based on probe

    return voltage

# converts twos compliment number
def twos_comp(val):
    if (val & (1 << (15))) != 0:
        val = val - (1 << 16)
    return val


def get_sample():
    val = read_data()
    voltage = conv_voltage(val)
    mag = conv_magnetic(voltage)
    return mag


