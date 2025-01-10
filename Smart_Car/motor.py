"""
使用方法：给定三个控制引脚创建Motor_Pin对象，再传入左右电机的引脚对象，创建Motor对象。
可使用MoveAhead、MoveBack、TurnLeft、TurnRight、MoveLeft、MoveRight、Stop方法控制小车。
"""
from gpiozero import PWMOutputDevice, DigitalOutputDevice

# 定义motor引脚类
class Motor_Pin:
    def __init__(self, pwm_pin, in1_pin, in2_pin):
        self.pwm = PWMOutputDevice(pwm_pin, frequency=1000)
        self.in1 = DigitalOutputDevice(in1_pin)
        self.in2 = DigitalOutputDevice(in2_pin)

# 定义motor类
class Motor:
    def __init__(self, left_motor: Motor_Pin, right_motor: Motor_Pin):
        self.__left_motor = left_motor
        self.__right_motor = right_motor

    def __left_ahead(self, speed: float):
        self.__left_motor.in1.on()
        self.__left_motor.in2.off()
        self.__left_motor.pwm.value = speed

    def __left_back(self, speed: float):
        self.__left_motor.in1.off()
        self.__left_motor.in2.on()
        self.__left_motor.pwm.value = speed

    def __right_ahead(self, speed: float):
        self.__right_motor.in1.on()
        self.__right_motor.in2.off()
        self.__right_motor.pwm.value = speed

    def __right_back(self, speed: float):
        self.__right_motor.in1.off()
        self.__right_motor.in2.on()
        self.__right_motor.pwm.value = speed

    def MoveAhead(self, speed: float):
        """
        Move the motor forward.
        :param speed: The speed of the motor (0.0 to 1.0)
        """
        self.__left_ahead(speed)
        self.__right_ahead(speed)

    def MoveBack(self, speed: float):
        """
        Move the motor backward.
        :param speed: The speed of the motor (0.0 to 1.0)
        """
        self.__left_back(speed)
        self.__right_back(speed)

    def TurnLeft(self, speed: float):
        """
        Left rotate.
        :param speed: The speed of the motor (0.0 to 1.0)
        """
        self.__left_back(min(speed * 0.2 + 0.8, 1.0))
        self.__right_ahead(min(speed * 0.2 + 0.8, 1.0))

    def TurnRight(self, speed: float):
        """
        Right rotate.
        :param speed: The speed of the motor (0.0 to 1.0)
        """
        self.__left_ahead(min(speed * 0.2 + 0.8, 1.0))
        self.__right_back(min(speed * 0.2 + 0.8, 1.0))

    def MoveLeft(self, speed: float):
        """
        Move the motor left.
        :param speed: The speed of the motor (0.0 to 1.0)
        """
        self.__left_ahead(speed * 0.8)
        self.__right_ahead(speed)

    def MoveRight(self, speed: float):
        """
        Move the motor right.
        :param speed: The speed of the motor (0.0 to 1.0)
        """
        self.__left_ahead(speed)
        self.__right_ahead(speed * 0.8)

    def Stop(self):
        """
        Stop the motor.
        """
        self.__left_motor.pwm.value = 0
        self.__right_motor.pwm.value = 0

    def Clean(self):
        """
        Release the pin resource
        """
        self.__left_motor.pwm.close()
        self.__left_motor.in1.close()
        self.__left_motor.in2.close()

        self.__right_motor.pwm.close()
        self.__right_motor.in1.close()
        self.__right_motor.in2.close()