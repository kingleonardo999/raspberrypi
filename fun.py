import RPi.GPIO as GPIO
import time
import random

GPIO.setmode(GPIO.BOARD)

led = 11
button = 12

GPIO.setup(led, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

time.sleep(3)

while True:
    if random.randint(1, 20) == 3:
        GPIO.output(led, GPIO.HIGH)
        start = time.time()
        while True:
            if not GPIO.input(button):
                end = time.time()
                GPIO.output(led, GPIO.LOW)
                print("Time costs " + str(round((end - start), 4)), end=" s")
                break
        break
GPIO.cleanup()