from class_pong import *
from classes_objects import *

def PaddleWall(player: Paddle):
    player.ComputeBoundingbox()

    if (player.boundingbox_top > 1.):
        player.position[1] -= player.boundingbox_top - 1.
    elif (player.boundingbox_bottom < -1.):
        player.position[1] += -(player.boundingbox_bottom + 1.)

def BallWall(ball: Ball):
    ball.ComputeBoundingbox()

    if (ball.boundingbox_left <= -1.):
        ball.direction[0] = abs(ball.direction[0]);
        ball.Reset()
        ball.collided = True
        # score[1] += 1;
    elif (ball.boundingbox_right >= 1.):
        ball.direction[0] = -abs(ball.direction[0])
        ball.Reset()
        ball.collided = True
    elif (ball.boundingbox_top >= 1.):
        ball.direction[1] = -abs(ball.direction[1])
        ball.collided = True
    elif (ball.boundingbox_bottom <= -1.):
        ball.direction[1] = abs(ball.direction[1])
        ball.collided = True