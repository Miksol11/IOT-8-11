#!/usr/bin/env python3

# pylint: disable=no-member

import time
import RPi.GPIO as GPIO
from config import *  # pylint: disable=unused-wildcard-import
from mfrc522 import MFRC522
import datetime
import board
import neopixel
import paho.mqtt.client as mqtt

REQUIRED_STABLE_READS = 5

broker = "localhost"
topic = "rfid/card"
client = mqtt.Client()

card_present = False
pixels = neopixel.NeoPixel(
        board.D18, 8, brightness=1.0/32, auto_write=False)
stable_reads = 0

def effects(state):
    global pixels
    GPIO.output(buzzerPin, not state)
    if state:
        pixels.fill((0, 0, 255))
        pixels.show()
    else:
        pixels.fill((0, 0, 0))
        pixels.show()

def uidToInt(uid):
    num = 0
    for i in range(len(uid)):
        num += uid[i] << (i * 8)
    return num

def rfidRead(MIFAREReader):
    global card_present, stable_reads

    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    if status == MIFAREReader.MI_OK:
        (status, uid) = MIFAREReader.MFRC522_Anticoll()
        if status == MIFAREReader.MI_OK:
            stable_reads = 0
            uid_num = uidToInt(uid)
            if not card_present:
                message = f"{uid_num};{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}"
                print(f"Wysłano: {message}")
                client.publish(topic, message)
                effects(True)
                time.sleep(0.2)
                effects(False)
                card_present = True

        return
    else:
        stable_reads += 1
        if(stable_reads >= REQUIRED_STABLE_READS):
            card_present = False  

def setupMFRC():
    client.connect(broker)
    MIFAREReader = MFRC522()
    return MIFAREReader

def closeMFRC():
    client.disconnect()

if __name__ == "__main__":
    MIFAREReader = setupMFRC()
    try:
        while True:
            rfidRead(MIFAREReader)
            time.sleep(0.05)
    except KeyboardInterrupt:
        closeMFRC()
    finally:
        GPIO.cleanup()