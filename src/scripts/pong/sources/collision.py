import copy
from class_game import *
from classes_objects import *
from class_vec2 import Vec2
from collision_utils import DoIntersect
from constants import *

def PaddleWall(player: Paddle):
    player.ComputeBoundingbox()

    if (player.boundingbox_top > 1.):
        player.position.y -= player.boundingbox_top - 1.
    elif (player.boundingbox_bottom < -1.):
        player.position.y += -(player.boundingbox_bottom + 1.)

def BallWall(ball: Ball):
    ball.ComputeBoundingbox()

    if (ball.boundingbox_left <= -1.):
        ball.direction.x = abs(ball.direction.x);
        ball.Reset()
        ball.collided = True
        # score[1] += 1;
    elif (ball.boundingbox_right >= 1.):
        ball.direction.x = -abs(ball.direction.x)
        ball.Reset()
        ball.collided = True
    elif (ball.boundingbox_top >= 1.):
        ball.direction.y = -abs(ball.direction.y)
        ball.collided = True
    elif (ball.boundingbox_bottom <= -1.):
        ball.direction.y = abs(ball.direction.y)
        ball.collided = True

def BallPaddle(ball: Ball, paddle: Paddle):
    ball.ComputeBoundingbox()
    paddle.ComputeBoundingbox()

    does_intersect = False;

    if ball.direction.x < 0.:
        if ball.direction.y < 0.: # ball y negatif
            # bottom current ball
            does_intersect = DoIntersect(
                Vec2(ball.previous_position.x + ball.radius, (ball.previous_position.y + ball.radius) * kScalingFactor[1]),
                Vec2(ball.boundingbox_left, ball.boundingbox_bottom),
                Vec2(paddle.boundingbox_right, paddle.boundingbox_bottom),
                Vec2(paddle.boundingbox_left, paddle.boundingbox_top)
            )
            if does_intersect == False:
                # top current ball
                does_intersect = DoIntersect(
                    Vec2(ball.previous_position.x + ball.radius, (ball.previous_position.y + ball.radius) * kScalingFactor[1]),
                    Vec2(ball.boundingbox_left, ball.boundingbox_top),
                    Vec2(paddle.boundingbox_right, paddle.boundingbox_bottom),
                    Vec2(paddle.boundingbox_left, paddle.boundingbox_top)
                )
        else: # ball y positif
            # top current ball
            does_intersect = DoIntersect(
                Vec2(ball.previous_position.x + ball.radius, (ball.previous_position.y - ball.radius) * kScalingFactor[1]),
                Vec2(ball.boundingbox_left, ball.boundingbox_top),
                Vec2(paddle.boundingbox_left, paddle.boundingbox_bottom),
                Vec2(paddle.boundingbox_right, paddle.boundingbox_top)
            )
            if does_intersect == False:
                # bottom current ball
                does_intersect = DoIntersect(
                    Vec2(ball.previous_position.x + ball.radius, (ball.previous_position.y - ball.radius) * kScalingFactor[1]),
                    Vec2(ball.boundingbox_left, ball.boundingbox_bottom),
                    Vec2(paddle.boundingbox_left, paddle.boundingbox_bottom),
                    Vec2(paddle.boundingbox_right, paddle.boundingbox_top)
                )

    if ball.direction.x >= 0.:
        if ball.direction.y < 0.: # ball y negatif
            # bottom current ball
            does_intersect = DoIntersect(
                Vec2(ball.previous_position.x - ball.radius, (ball.previous_position.y + ball.radius) * kScalingFactor[1]),
                Vec2(ball.boundingbox_right, ball.boundingbox_bottom),
                Vec2(paddle.boundingbox_right, paddle.boundingbox_top),
                Vec2(paddle.boundingbox_left, paddle.boundingbox_bottom)
            )
            # top current ball
            if does_intersect == False:
                does_intersect = DoIntersect(
                    Vec2(ball.previous_position.x - ball.radius, (ball.previous_position.y + ball.radius) * kScalingFactor[1]),
                    Vec2(ball.boundingbox_right, ball.boundingbox_top),
                    Vec2(paddle.boundingbox_right, paddle.boundingbox_top),
                    Vec2(paddle.boundingbox_left, paddle.boundingbox_bottom)
            )
        else: # ball y positif
            # top current ball
            does_intersect = DoIntersect(
                Vec2(ball.previous_position.x - ball.radius, (ball.previous_position.y - ball.radius) * kScalingFactor[1]),
                Vec2(ball.boundingbox_right, ball.boundingbox_top),
                Vec2(paddle.boundingbox_left, paddle.boundingbox_top),
                Vec2(paddle.boundingbox_right, paddle.boundingbox_bottom)
            )
            # bottom current ball
            if does_intersect == False:
                does_intersect = DoIntersect(
                    Vec2(ball.previous_position.x - ball.radius, (ball.previous_position.y - ball.radius) * kScalingFactor[1]),
                    Vec2(ball.boundingbox_right, ball.boundingbox_bottom),
                    Vec2(paddle.boundingbox_left, paddle.boundingbox_top),
                    Vec2(paddle.boundingbox_right, paddle.boundingbox_bottom)
                )
 

    if does_intersect == True:
        if ball.direction.x < 0.:
            ball.position.x = paddle.boundingbox_right + ball.radius
        else:
            ball.position.x = paddle.boundingbox_left - ball.radius
        ball.direction.x = -ball.direction.x
        ball.acceleration += kBallAccelerationStep
        if paddle.key == DATA_INPUT_KEY_UP:
            ball.direction.y = 1.
        elif paddle.key == DATA_INPUT_KEY_DOWN:
            ball.direction.y = -1.
        ball.previous_position = Vec2(0., 0.)
        ball.collided = True
    else:
        if paddle.position.x > 0.: # After second player
            ball.previous_position = copy.deepcopy(ball.position)


    return does_intersect