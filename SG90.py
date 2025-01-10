import RPi.GPIO as GPIO
import time

GPIO.cleanup()

GPIO.setmode(GPIO.BCM)

pwm_pin1 = 20
pwm_pin2 = 21

GPIO.setup(pwm_pin1, GPIO.OUT)
GPIO.setup(pwm_pin2, GPIO.OUT)

pwm1 = GPIO.PWM(pwm_pin1, 50)
pwm2 = GPIO.PWM(pwm_pin2, 50)

pwm1.start(0)
pwm2.start(0)

def set_angleup(angle):
    duty_cycle = (angle / 18.0) + 2.5
    pwm2.ChangeDutyCycle(duty_cycle)
    time.sleep(0.05)
    pwm2.ChangeDutyCycle(0)

def set_angledown(angle):
    duty_cycle = (angle / 18.0) + 2.5
    pwm1.ChangeDutyCycle(duty_cycle)
    time.sleep(0.05)
    pwm1.ChangeDutyCycle(0)