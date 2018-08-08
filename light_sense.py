import spidev
import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
LED=3
GPIO.setup(LED,GPIO.OUT,initial=GPIO.LOW)

spi=spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000

delay = 5

def ReadChannel(channel):
    adc=spi.xfer2([1, (8+channel)<<4,0])
    data = ((adc[1]&3 <<8) +adc[2])
    return data

def ConvertLight(data,places):
    volts = ((data*330)/float(1023))
    light = round(volts,places)
    return light

light_channel = 0

while True:
    light_level = ReadChannel(light_channel)
    light = ConvertLight(light_level,2)

    print("--------------------------")
    print("Light: {} {}".format(light_level, light))
        
    if light_level<150:
        GPIO.output(LED,GPIO.HIGH)
        print("LED is on!")
    else:
        GPIO.output(LED,GPIO.LOW)
        print("LED is off :(")
        
    time.sleep(delay)
