# Drew's CO2 monitoring DEF CON badge/mask
# A lot of this code is taken from other Adafruit code examples, kinda a frankencode...
# I need to move some pins around so that I can use the buttons on the OLED display to do things, like run a calibration routine

import time
import board
import busio
import adafruit_scd30
import displayio
import adafruit_imageload
import terminalio
import adafruit_displayio_sh1107
from adafruit_st7789 import ST7789
from rainbowio import colorwheel
import neopixel
from analogio import AnalogIn
# can try import bitmap_label below for alternative
from adafruit_display_text import bitmap_label

# --| User Config |----
CO2_CUTOFFS = (1000, 2000, 5000)
UPDATE_RATE = 0.5
# ---------------------

# SCD-30 has tempremental I2C with clock stretching, datasheet recommends
# starting at 50KHz
#i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
scd30 = adafruit_scd30.SCD30(board.I2C())
#scd30.temperature_offset = 0 # thinking of making a separate calibration routine

# Lets get the battery voltage
vbat_voltage = AnalogIn(board.VOLTAGE_MONITOR)

# Let's define some functions
# First let's get the battery voltage
def get_voltage(pin):
    return (pin.value * 3.3) / 65536 * 2

# onboard neopixel color change based on level and blink if over level 4
def pixel0_color(value):
    if scd30.CO2 < CO2_CUTOFFS[0]:
        pixel0.fill((0,255,0))
        pixel0.show()
    elif scd30.CO2 < CO2_CUTOFFS[1]:
        pixel0.fill((255,255,0))
        pixel0.show()
    elif scd30.CO2 < CO2_CUTOFFS[2]:
        pixel0.fill((255,0,0))
        pixel0.show()
    else:
        pixel0.fill((255,0,0))
        pixel0.show()
        time.sleep(0.25)
        pixel0.fill((0,0,0))
        pixel0.show()
        time.sleep(0.25)

# mask neopixel color change based on level and blink if over level 4
def pixel1_color(value):
    if scd30.CO2 < CO2_CUTOFFS[0]:
        pixel1.fill((255,0,0,0))
        pixel1.show()
    elif scd30.CO2 < CO2_CUTOFFS[1]:
        pixel1.fill((255,255,0,0))
        pixel1.show()
    elif scd30.CO2 < CO2_CUTOFFS[2]:
        pixel1.fill((0,255,0,0))
        pixel1.show()
    else:
        pixel1.fill((64,255,0,0))
        pixel1.show()
        time.sleep(0.5)
        pixel1.fill((0,0,0,0))
        pixel1.show()
        time.sleep(0.125)

# Mask Display update
def update_display(value):

    value = abs(round(value))

    # smiley and label
    if value < CO2_CUTOFFS[0]:
        smiley[0] = label[0] = 0
    elif value < CO2_CUTOFFS[1]:
        smiley[0] = label[0] = 1
    elif value < CO2_CUTOFFS[2]:
        smiley[0] = label[0] = 2
    else:
        smiley[0] = label[0] = 3

    # CO2 value
    # clear it
    for i in range(4):
        co2_value[i] = 10
    # update it
    i = 3
    while value:
        co2_value[i] = value % 10
        value = int(value / 10)
        i -= 1

# release any currently configured displays
displayio.release_displays()

# setup fourwire for TFT display
spi = board.SPI()
tft_cs = board.D5
tft_dc = board.D9

# setup displays
display_bus0 = displayio.I2CDisplay(board.I2C(), device_address=0x3C)
display_bus1 = displayio.FourWire(
     spi, command=tft_dc, chip_select=tft_cs, reset=board.D6
)

# Define the first display
# SH1107 is vertically oriented 64x128 set as display0
display0 = adafruit_displayio_sh1107.SH1107(
    display_bus0, width=128, height=64, rotation=0
)

# Lets give display0 some output
# create labels and do some math
co2 = "CO2: %d PPM" % scd30.CO2
#temperature = "Temp: %0.2f Degrees F" % ((scd30.temperature* 9/5) + 32)
temperature = "Temp: %0.2f Degrees C" % scd30.temperature
humidity = "Humidity: %0.2f %% rH" % scd30.relative_humidity
battery_voltage = "Batt: %0.2f VDC" % get_voltage(vbat_voltage)

# Draw some label text
co2_line = bitmap_label.Label(terminalio.FONT, text=co2, scale=1, color=0xFFFFFF, x=2, y=4)
temp_line = bitmap_label.Label(terminalio.FONT, text=temperature, scale=1, color=0xFFFFFF, x=2, y=19)
humidity = bitmap_label.Label(terminalio.FONT, text=humidity, scale=1, color=0xFFFFFF, x=2, y=34)
battery_voltage = bitmap_label.Label(terminalio.FONT, text=battery_voltage, scale=1, color=0xFFFFFF, x=2, y=49)

# Make the display context and show the data
splash0 = displayio.Group()
splash0.append(co2_line)
splash0.append(temp_line)
splash0.append(humidity)
splash0.append(battery_voltage)
display0.show(splash0)

# # define second display
display1 = ST7789(display_bus1, width=240, height=320, rotation=180)

# Let's put some content on Display1
# current condition smiley face
smileys_bmp, smileys_pal = adafruit_imageload.load("/bmps/smileys.bmp")
smiley = displayio.TileGrid(
    smileys_bmp,
    pixel_shader=smileys_pal,
    x=20,
    y=0,
    width=1,
    height=1,
    tile_width=200,
    tile_height=200,
)
#Like co2line above but we want bigger text
#I'm trying to get the CO2 value label to stay centered, but this isn't working...
# def co2_level(value):
#     if scd30.CO2 < CO2_CUTOFFS[0]:
#         bitmap_label.Label(terminalio.FONT, text="%d" % scd30.CO2, scale=6, color=0xFFFFFF, x=66, y=275)
#     else:
#         bitmap_label.Label(terminalio.FONT, text="%d" % scd30.CO2, scale=6, color=0xFFFFFF, x=48, y=275)

co2_label = bitmap_label.Label(terminalio.FONT, text="CO2 PPM", scale=4, color=0xFFFFFF, x=38, y=220)
co2_level = bitmap_label.Label(terminalio.FONT, text="%d" % scd30.CO2, scale=6, color=0xFFFFFF, x=66, y=275)


# Lets setup display1 context and show the data
splash1 = displayio.Group()
splash1.append(smiley)
splash1.append(co2_label)
splash1.append(co2_level)
display1.show(splash1)

# setup neopixels
# onboard neopixel
pixel0 = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.01)
# mask neopixels
# uncomment when connected dont forget to set pin...
pixel1 = neopixel.NeoPixel(board.D10, 48, pixel_order=neopixel.RGBW, brightness=0.01)

# Let's light this candle
while True:
    #Update onboard display values
    co2_line.text = "CO2: %d PPM" % scd30.CO2
    #temp_line.text = "Temp: %0.2f Degrees F" % ((scd30.temperature* 9/5) + 32)
    temp_line.text = "Temp: %0.2f Degrees C" % scd30.temperature
    humidity.text = "Humidity: %0.2f %% rH" % scd30.relative_humidity
    battery_voltage.text = "Batt: %0.2f VDC" % get_voltage(vbat_voltage)
    co2_level.text = "%d" % scd30.CO2
    pixel0_color(scd30.CO2)
    pixel1_color(scd30.CO2)
    # protect against NaNs and Nones
    try:
        update_display(scd30.CO2)

    except:
        pass
    time.sleep(UPDATE_RATE)
