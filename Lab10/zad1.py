#!/usr/bin/env python3

import time
from PIL import Image, ImageDraw, ImageFont
import lib.oled.SSD1331 as SSD1331
from config import *
import board
import busio
import adafruit_bme280.advanced as adafruit_bme280
import RPi.GPIO as GPIO

def printOnDisplay(temperature, pressure, humidity, altitude, disp):
    image = Image.new("RGB", (disp.width, disp.height), "White")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('./lib/oled/Font.ttf', 14)
    dictionary = {'Temperature': temperature, 'Pressure': pressure, 'Humidity': humidity, 'Altitude': altitude}
    height = 0
    for key in dictionary:
        icon = Image.open(f'Lab10/icons/{key}.png')
        image.paste(icon, (0, height), icon)
        draw.text((18, height), f"{dictionary[key]}", font=font, fill="BLACK")
        height+=16

    disp.ShowImage(image, 0, 0)

def measurements(bme280, disp):
    temperature = f"{bme280.temperature:0.1f}" + chr(176) + "C"
    pressure = f"{bme280.pressure:0.1f}hPa"
    humidity = f"{bme280.humidity:0.1f}%"
    altitude = f"{bme280.altitude:0.2f} meters"
    printOnDisplay(temperature, pressure, humidity, altitude, disp)

def setupDisp():
    disp = SSD1331.SSD1331()

    disp.Init()
    disp.clear()

    return disp

def setupBME():
    i2c = busio.I2C(board.SCL, board.SDA)
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x76)

    bme280.sea_level_pressure = 1013.25
    bme280.standby_period = adafruit_bme280.STANDBY_TC_500
    bme280.iir_filter = adafruit_bme280.IIR_FILTER_X16
    bme280.overscan_pressure = adafruit_bme280.OVERSCAN_X16
    bme280.overscan_humidity = adafruit_bme280.OVERSCAN_X1
    bme280.overscan_temperature = adafruit_bme280.OVERSCAN_X2
    return bme280


if __name__ == "__main__":
    disp = setupDisp()
    bme280 = setupBME()
    try:
        while True:
            measurements(bme280, disp)
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        disp.clear()
        disp.reset()
        GPIO.cleanup()
