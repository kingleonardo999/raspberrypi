import RPi.GPIO as GPIO
import time

# 设置GPIO模式为BCM编号
GPIO.setmode(GPIO.BCM)

# 定义按键所连接的GPIO引脚
button_pin = 17

# 设置按键引脚为输入模式，并启用内部上拉电阻
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        # 检查按键是否被按下
        if not GPIO.input(button_pin):  # 如果按键被按下，读数会变为低电平（False）
            print("Button Pressed")
            # 等待按键释放
            while not GPIO.input(button_pin):
                time.sleep(0.1)
        time.sleep(0.1)  # 避免过于频繁的轮询

except KeyboardInterrupt:
    # 当用户通过Ctrl+C中断程序时执行清理工作
    print()
    print("Program terminated by user.")
finally:
    # 清理GPIO设置
    GPIO.cleanup()