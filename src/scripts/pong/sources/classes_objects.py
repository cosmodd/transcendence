from constants import *
from class_vec2 import Vec2

class Ball:
    def __init__(self, direction=Vec2(0., 0.)):
        self.position = Vec2(0., 0.)
        self.previous_position = Vec2(0., 0.)
        self.radius = kBallRadius
        self.speed = kBallSpeed
        self.acceleration = 0.
        self.direction = direction
        self.collided = False
        #self.accelerationStep
    
    def Reset(self):
        self.position = Vec2(0., 0.)
        self.direction = Vec2(-1., 0.)
        self.acceleration = 0.;

    def ComputeBoundingbox(self):
        self.boundingbox_left = self.position.x - self.radius;
        self.boundingbox_right = self.position.x + self.radius;
        self.boundingbox_top = self.position.y + self.radius;
        self.boundingbox_bottom = self.position.y - self.radius;
        self.boundingbox_left *= kScalingFactor[0]
        self.boundingbox_right *= kScalingFactor[0];
        self.boundingbox_top *= kScalingFactor[1];
        self.boundingbox_bottom *= kScalingFactor[1];

class Paddle:
    def __init__(self, position: Vec2):
        self.position = position
        self.speed = kPaddleSpeed
        self.width_half = kPaddleWidth / 2.0
        self.height_half = kPaddleHeight / 2.0
        self.key = DATA_INPUT_KEY_NONE
        self.key_has_changed = False

    def ComputeBoundingbox(self):
        self.boundingbox_left = self.position.x - self.width_half;
        self.boundingbox_right = self.position.x + self.width_half;
        self.boundingbox_top = self.position.y + self.height_half;
        self.boundingbox_bottom = self.position.y - self.height_half;
        self.boundingbox_left *= kScalingFactor[0]
        self.boundingbox_right *= kScalingFactor[0];
        self.boundingbox_top *= kScalingFactor[1];
        self.boundingbox_bottom *= kScalingFactor[1];

