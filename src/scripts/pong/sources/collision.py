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
        ball.direction.x = abs(ball.direction.y)
        ball.collided = True

last_ball_pos = None;
def BallPaddle(ball: Ball, paddle: Paddle):
    global last_ball_pos
    ball.ComputeBoundingbox()
    paddle.ComputeBoundingbox()

    if last_ball_pos is None:
        last_ball_pos = ball.position.Clone()
        return

    does_intersect = False;
    if ball.direction.y < 0.: # ball y negatif
        # bottom current ball
        does_intersect = DoIntersect(
            Vec2(last_ball_pos.x + ball.radius, (last_ball_pos.y + ball.radius) * kScalingFactor[1]),
            Vec2(ball.boundingbox_left, ball.boundingbox_bottom),
            Vec2(paddle.boundingbox_right, paddle.boundingbox_bottom),
            Vec2(paddle.boundingbox_left, paddle.boundingbox_top)
        )
        # top current ball
        does_intersect = DoIntersect(
            Vec2(last_ball_pos.x + ball.radius, (last_ball_pos.y + ball.radius) * kScalingFactor[1]),
            Vec2(ball.boundingbox_left, ball.boundingbox_top),
            Vec2(paddle.boundingbox_right, paddle.boundingbox_bottom),
            Vec2(paddle.boundingbox_left, paddle.boundingbox_top)
        )
    else: # ball y positif
        # top current ball
        does_intersect = DoIntersect(
            Vec2(last_ball_pos.x + ball.radius, (last_ball_pos.y - ball.radius) * kScalingFactor[1]),
            Vec2(ball.boundingbox_left, ball.boundingbox_top),
            Vec2(paddle.boundingbox_left, paddle.boundingbox_bottom),
            Vec2(paddle.boundingbox_right, paddle.boundingbox_top)
        )
        # bottom current ball
        does_intersect = DoIntersect(
            Vec2(last_ball_pos.x + ball.radius, (last_ball_pos.y - ball.radius) * kScalingFactor[1]),
            Vec2(ball.boundingbox_left, ball.boundingbox_bottom),
            Vec2(paddle.boundingbox_left, paddle.boundingbox_bottom),
            Vec2(paddle.boundingbox_right, paddle.boundingbox_top)
        )
    if does_intersect:
        ball.direction.x = -ball.direction.x
        ball.position.x = paddle.boundingbox_right + ball.radius
        ball.acceleration += kBallAccelerationStep
        if paddle.key == DATA_INPUT_KEY_UP:
            ball.direction.y = 1.
        elif paddle.key == DATA_INPUT_KEY_DOWN:
            ball.direction.y = -1.
        last_ball_pos = None
        ball.collided = True
    else:
        last_ball_pos = ball.position.Clone()