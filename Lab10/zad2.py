#!/usr/bin/env python3

# pylint: disable=no-member

import time
import RPi.GPIO as GPIO
from config import *  # pylint: disable=unused-wildcard-import
from mfrc522 import MFRC522
import datetime
import board
import neopixel

card_present = False
last_time = time.time()
pixels = neopixel.NeoPixel(
        board.D18, 8, brightness=1.0/32, auto_write=False)

def effects(state):
    global pixels
    GPIO.output(buzzerPin, not state)
    if state:
        pixels.fill((0, 0, 255))
        pixels.show()
    else:
        pixels.fill((0, 0, 0))
        pixels.show()

def uid_to_int(uid):
    num = 0
    for i in range(len(uid)):
        num += uid[i] << (i * 8)
    return num

def rfidRead(MIFAREReader):
    global card_present, last_time

    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    if status == MIFAREReader.MI_OK:
        (status, uid) = MIFAREReader.MFRC522_Anticoll()
        if status == MIFAREReader.MI_OK:
            uid_num = uid_to_int(uid)
            last_time = time.time()
            if not card_present:
                print("UID: ", uid_num, " Time: ", datetime.datetime.now().strftime("%H:%M:%S"))
                effects(True)
                time.sleep(1)
                effects(False)
                card_present = True
    else:
        if(time.time() - last_time >= 0.2):
            card_present = False
        

def setupMFRC():
    MIFAREReader = MFRC522()
    return MIFAREReader

if __name__ == "__main__":
    MIFAREReader = setupMFRC()
    try:
        while True:
            rfidRead(MIFAREReader)
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()