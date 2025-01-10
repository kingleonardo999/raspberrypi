import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
led = 11
button = 12
GPIO.setup(led, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(button, GPIO.IN, pull_up_down = GPIO.PUD_UP)

try:
    while True:
        if not GPIO.input(button):  # 如果按键被按下，读数会变为低电平（False）
            print("Button Pressed")
            if GPIO.input(led) == GPIO.LOW:
                GPIO.output(led, GPIO.HIGH)
            else:
                GPIO.output(led, GPIO.LOW)
            # 等待按键释放
            while not GPIO.input(button):
                time.sleep(0.1)
        time.sleep(0.1)  # 避免过于频繁的轮询

except KeyboardInterrupt:
    # 当用户通过Ctrl+C中断程序时执行清理工作
    print()
    print("Program terminated by user.")
finally:
    # 清理GPIO设置
    GPIO.cleanup()