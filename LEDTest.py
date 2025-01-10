import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(12, GPIO.IN)

flag = False

GPIO.output(11, GPIO.HIGH)
time.sleep(2)
GPIO.output(11, GPIO.LOW)
GPIO.cleanup()

while True:
    try:
        if GPIO.input(12):
            time.sleep(1)
            if flag:
                flag = False
                GPIO.output(11, GPIO.LOW)
            else:
                flag = True
                GPIO.output(11, GPIO.HIGH)
    except KeyboardInterrupt:
        GPIO.cleanup()