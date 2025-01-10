import time

# PID控制器
class PID:
    def __init__(self, kP, kI, kD=0):
        self.kP = kP
        self.kI = kI
        self.kD = kD
        self.prevError = 0
        self.prevTime = None
        self.cP = 0
        self.cI = 0
        self.cD = 0

    def initialize(self):
        self.prevTime = time.time()

    def update(self, error, sleep=0.02):
        time.sleep(sleep)
        currTime = time.time()
        deltaTime = currTime - self.prevTime if self.prevTime is not None else 0
        deltaError = error - self.prevError

        self.cP = error
        self.cI += error * deltaTime
        self.cD = (deltaError / deltaTime) if deltaTime > 0 else 0

        self.prevTime = currTime
        self.prevError = error

        return self.kP * self.cP + self.kI * self.cI + self.kD * self.cD