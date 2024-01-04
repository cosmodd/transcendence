from constants import *

class Ball:
    def __init__(self, position, speed=0.0, acceleration=0.0):
        self.position = position
        self.speed = speed
        self.acceleration = acceleration
        #self.accelerationStep

class Paddle:
    def __init__(self, position):
        self.position = position
        self.speed = kPaddleSpeed
        self.key = DATA_INPUT_KEY_NONE
        self.has_key_changed = False

