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
        self.width_half = kPaddleWidth / 2.0
        self.height_half = kPaddleHeight / 2.0
        self.key = DATA_INPUT_KEY_NONE
        self.key_has_changed = False

    def ComputeBoundingbox(self):
        self.boundingbox_left = self.position[0] - self.width_half;
        self.boundingbox_right = self.position[0] + self.width_half;
        self.boundingbox_top = self.position[1] + self.height_half;
        self.boundingbox_bottom = self.position[1] - self.height_half;
        self.boundingbox_left *= kScalingFactor[0]
        self.boundingbox_right *= kScalingFactor[0];
        self.boundingbox_top *= kScalingFactor[1];
        self.boundingbox_bottom *= kScalingFactor[1];

