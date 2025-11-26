from config import *
import RPi.GPIO as GPIO
import time

number_of_leds = 4
hz = 50
active_led = 0
debounce_time = 200
intensity = [50, 50, 50, 50]
diodes = [GPIO.PWM(led1, hz), GPIO.PWM(led2, hz), GPIO.PWM(led3, hz), GPIO.PWM(led4, hz)]

def changeLED(step: int):
    global active_led
    diodes[active_led].ChangeDutyCycle(0)
    active_led = (active_led + step) % number_of_leds
    diodes[active_led].ChangeDutyCycle(intensity[active_led])

def changeIntensity(step: int):
    intensity[active_led] = max(0, min(intensity[active_led] + step, 100))
    diodes[active_led].ChangeDutyCycle(intensity[active_led])

def stopAllDiodes():
    for diode in diodes:
        diode.stop()
    GPIO.cleanup()

def startAllDiodes():
    for diode in diodes:
        diode.start(0)
        
def setup():
    GPIO.add_event_detect(buttonRed, GPIO.FALLING, callback=lambda l: changeLED(-1), bouncetime=debounce_time)
    GPIO.add_event_detect(buttonGreen, GPIO.FALLING, callback=lambda l: changeLED(1), bouncetime=debounce_time)

    GPIO.add_event_detect(encoderLeft, GPIO.FALLING, callback=lambda l: changeIntensity(10), bouncetime=debounce_time)
    GPIO.add_event_detect(encoderRight, GPIO.FALLING, callback=lambda l: changeIntensity(-10), bouncetime=debounce_time)

    startAllDiodes()
    changeLED(0)

if __name__ == "__main__":
    setup()
    try:
        while True:
            print(f"Aktualna intensywność: {intensity[active_led]}%")
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        stopAllDiodes()