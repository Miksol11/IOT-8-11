#!/usr/bin/env python3

# Wykorzystując treść opisaną w lab09.pdf proszę o wykonanie zadania:
# Napisz program, który zmierzy temperaturę, ciśnienie i wilgotność. Wartości te mają się wyświetlać na konsoli. 
# Dodatkowo korzystając z wzoru na wysokość barometryczną (https://ep.com.pl/projekty/projekty-ep/15452-wysokosciomierz-barometryczny)
# proszę obliczyć aktualną wysokość nad poziomem morza.

from config import *
import board
import busio
import adafruit_bme280.advanced as adafruit_bme280
import time
import os

def setup():
    i2c = busio.I2C(board.SCL, board.SDA)
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x76)

    bme280.sea_level_pressure = 1013.25
    bme280.standby_period = adafruit_bme280.STANDBY_TC_500
    bme280.iir_filter = adafruit_bme280.IIR_FILTER_X16
    bme280.overscan_pressure = adafruit_bme280.OVERSCAN_X16
    bme280.overscan_humidity = adafruit_bme280.OVERSCAN_X1
    bme280.overscan_temperature = adafruit_bme280.OVERSCAN_X2

    return bme280

def measurements(bme280):
    # os.system("clear") #Raspberry
    os.system("cls") #Windows

    altitude = 44330 * (1 - (bme280.pressure/bme280.sea_level_pressure) ** (1/5.255))

    print(f"Temperature: {bme280.temperature:0.1f}" + chr(176) + "C")
    print(f"Pressure: {bme280.pressure:0.1f} hPa")
    print(f"Humidity: {bme280.humidity:0.1f}%")
    print(f"Altitude: {altitude:0.2f} meters")

if __name__ == "__main__":
    bme280 = setup()
    try:
        while True:
            measurements(bme280)
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
