"""
通过PCA9685驱动舵机，默认使用硬件I2C总线，地址0x40
传入的参数channel是一个列表，用于指定要控制的舵机通道
注意使用时要添加延时，以免连续操作舵机产生抖动
"""
from adafruit_pca9685 import PCA9685
import board
import busio

# 舵机类
class Servo:
    def __init__(self, channel:list, i2c = busio.I2C(board.SCL, board.SDA)):
        """
        默认使用I2C总线，地址0x40
        :param channel: 指定的通道构成的列表
        :param i2c: 默认硬件I2C总线
        """
        self.channel = channel
        self.pca = PCA9685(i2c, address=0x40)  # 使用已知的I2C地址0x40
        self.pca.frequency = 50 # 设置PWM频率为50Hz（适合大多数舵机）

    def add_channel(self, channel_idx:int):
        """
        添加一个通道
        :param channel_idx: 指定的通道索引
        :return:
        """
        self.channel.append(channel_idx)

    def remove_channel(self, channel_idx:int):
        """
        移除一个通道
        :param channel_idx: 指定的通道索引
        :return:
        """
        self.channel.remove(channel_idx)

    def __angle_to_pwm(self, angle:float):
        # 计算脉冲宽度（在0.5ms至2.5ms之间），对应于0度到180度
        pulse_width = (angle / 180.0) * (2.5 - 0.5) + 0.5
        # 将脉冲宽度转换为16位的PWM值
        pwm_value = int(pulse_width / 20 * 0xFFFF)
        return pwm_value

    def set_angle(self, channle_idx:int, angle:float):
        """
        设置指定通道的舵机角度
        :param channle_idx:指定的通道索引
        :param angle: 设定的角度
        :return:
        """
        idx_in_channel = self.channel.index(channle_idx) # 获取通道在通道列表中的索引
        pwm_value = self.__angle_to_pwm(angle) # 将角度转换为PWM值
        self.pca.channels[self.channel[idx_in_channel]].duty_cycle = pwm_value # 设置PWM值