import smbus2
import time

# 创建SMBus对象
bus = smbus2.SMBus(1)  # 1 表示 /dev/i2c-1 或者 /dev/i2c-adapter1

# STM32的I2C地址
stm32_address = 0x32  # 请根据实际情况修改

try:
    write_data = [0x11, 0x10, 0x21, 0x20]
    while True:
        try:
            # 写入数据到STM32
            a = input("Enter data to write: ")
            b = int(a)
            bus.write_byte(stm32_address, write_data[b])
            print("Data sent to STM32: ", write_data[b])

            # 读取数据从STM32
            read_data = bus.read_byte(stm32_address)
            print("Data received from STM32: ", read_data)
        except OSError:
            print("I/O error")

except KeyboardInterrupt:
    pass
finally:
    bus.close()