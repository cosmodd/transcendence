import sys
import copy
from class_game import *
from classes_objects import *
from class_vec2 import Vec2
from collision_utils import DoIntersect, PaddleInterceptionPoint
from constants import *

class Collision:
    def __init__(self, game):
        self.attached_game = game

    def PaddleWall(self, player: Paddle):
        player.ComputeBoundingbox()

        if (player.boundingbox_top > 1.):
            player.position.y -= player.boundingbox_top - 1.
        elif (player.boundingbox_bottom < -1.):
            player.position.y += -(player.boundingbox_bottom + 1.)

    def BallWall(self, ball: Ball):
        ball.ComputeBoundingbox()

        if (ball.boundingbox_left <= -1.):
            ball.direction.x = abs(ball.direction.x);
            ball.Reset()
            ball.collided = True
            self.attached_game.UpdateScore(DATA_PLAYER_PLAYER2)
        elif (ball.boundingbox_right >= 1.):
            ball.direction.x = -abs(ball.direction.x)
            ball.Reset()
            ball.collided = True
            self.attached_game.UpdateScore(DATA_PLAYER_PLAYER1)
        elif (ball.boundingbox_top >= 1.):
            ball.direction.y = -abs(ball.direction.y)
            ball.collided = True
        elif (ball.boundingbox_bottom <= -1.):
            ball.direction.y = abs(ball.direction.y)
            ball.collided = True

    def BallPaddle(self, ball: Ball, paddle: Paddle):
        ball.ComputeBoundingbox()
        paddle.ComputeBoundingbox()

        does_intersect = False;
        intersect_type = "none";

		# Left Paddle
        if ball.direction.x <= 0.:
            # Paddle right side
            does_intersect = DoIntersect(
                Vec2(ball.previous_position.x + ball.radius, ball.previous_position.y * kScalingFactor[1]),
                Vec2(ball.boundingbox_left, ball.position.y),
                Vec2(paddle.boundingbox_right, paddle.boundingbox_bottom),
                Vec2(paddle.boundingbox_right, paddle.boundingbox_top))
            if (does_intersect == True):
                intersect_type = "side"
            # Paddle top
            if (does_intersect == False):
                does_intersect = DoIntersect(
                    Vec2(ball.previous_position.x, ball.previous_position.y * kScalingFactor[1]),
                    Vec2(ball.position.x, ball.position.y),
                    Vec2(paddle.boundingbox_right, paddle.boundingbox_top),
                    Vec2(paddle.boundingbox_left, paddle.boundingbox_top))
                if (does_intersect == True):
                    intersect_type = "top"
            # Paddle bottom
            if (does_intersect == False):
                does_intersect = DoIntersect(
                    Vec2(ball.previous_position.x, ball.previous_position.y * kScalingFactor[1]),
                    Vec2(ball.position.x, ball.position.y),
                    Vec2(paddle.boundingbox_right, paddle.boundingbox_bottom),
                    Vec2(paddle.boundingbox_left, paddle.boundingbox_bottom))
                if (does_intersect == True):
                    intersect_type = "bottom"

		# Right Paddle
        if ball.direction.x > 0.:
            # bottom current ball
            does_intersect = DoIntersect(
                Vec2(ball.previous_position.x - ball.radius, ball.previous_position.y * kScalingFactor[1]),
                Vec2(ball.boundingbox_right, ball.position.y),
                Vec2(paddle.boundingbox_left, paddle.boundingbox_top),
                Vec2(paddle.boundingbox_left, paddle.boundingbox_bottom))
            if (does_intersect == True):
                intersect_type = "side"
            # Paddle top
            if (does_intersect == False):
                does_intersect = DoIntersect(
                    Vec2(ball.previous_position.x, ball.previous_position.y * kScalingFactor[1]),
                    Vec2(ball.position.x, ball.position.y),
                    Vec2(paddle.boundingbox_right, paddle.boundingbox_top),
                    Vec2(paddle.boundingbox_left, paddle.boundingbox_top))
                if (does_intersect == True):
                    intersect_type = "top"
            # Paddle bottom
            if (does_intersect == False):
                does_intersect = DoIntersect(
                    Vec2(ball.previous_position.x, ball.previous_position.y * kScalingFactor[1]),
                    Vec2(ball.position.x, ball.position.y),
                    Vec2(paddle.boundingbox_right, paddle.boundingbox_bottom),
                    Vec2(paddle.boundingbox_left, paddle.boundingbox_bottom))
                if (does_intersect == True):
                    intersect_type = "bottom"

		# Intersection !
        if does_intersect == True:
            if (intersect_type == "side"):
                intersect = PaddleInterceptionPoint(ball, paddle, ball.previous_position)
                local_gap = intersect.y - paddle.position.y
                ball.position.x = paddle.boundingbox_right + ball.radius if ball.direction.x <= 0.0 else paddle.boundingbox_left - ball.radius;
                #ball.position.y = intersect.y
                ball.direction.x = -(ball.direction.x - sys.float_info.min)
                ball.direction.y += local_gap / paddle.height_half
                ball.direction.y = min(1.0, ball.direction.y)
                ball.direction.y = max(-1.0, ball.direction.y)
            elif (intersect_type == "top" or intersect_type == "bottom"):
                ball.position.y = paddle.boundingbox_top + ball.radius if intersect_type == "top" else paddle.boundingbox_bottom - ball.radius;
                ball.direction.x = -(ball.direction.x + sys.float_info.min)
                ball.direction.y = -(ball.direction.y + sys.float_info.min)
            ball.acceleration += kBallAccelerationStep
            ball.direction = ball.direction.Normalize()
            ball.previous_position = Vec2(0., 0.)
            ball.collided = True
        else:
            if paddle.position.x > 0.: # After second player
                ball.previous_position = copy.deepcopy(ball.position)

        return does_intersect