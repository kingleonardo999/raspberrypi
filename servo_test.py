from Smart_Car.motor import Motor, Motor_Pin
import time
# 定义motor类
motor = Motor(Motor_Pin(0, 5, 6), Motor_Pin(13, 19, 26))

# Move the motor forward.
# motor.MoveAhead(1)
# print("Move ahead")
# time.sleep(2)
# motor.MoveBack(1)
# print("Move back")
# time.sleep(2)
motor.TurnLeft(1)
print("Turn left")
time.sleep(2)
motor.TurnRight(1)
print("Turn right")
time.sleep(2)
motor.MoveLeft(1)
print("Move left")
time.sleep(2)
motor.MoveRight(1)
print("Move right")
time.sleep(2)

motor.Stop()
