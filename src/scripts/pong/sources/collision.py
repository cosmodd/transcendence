from class_pong import *
from classes_objects import *

def PaddleWall(player: Paddle):
    player.ComputeBoundingbox()

    if (player.boundingbox_top > 1.):
        player.position[1] -= player.boundingbox_top - 1.
    elif (player.boundingbox_bottom < -1.):
        player.position[1] += -(player.boundingbox_bottom + 1.)
