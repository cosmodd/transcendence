import json
from classes_objects import Ball, Paddle
from class_messagebuilder import MessageBuilder
from constants import *
from datetime import datetime
from class_vec2 import Vec2

__all__ = ["PLAYER1", "PLAYER2", "Game"]

PLAYER1, PLAYER2 = "p1", "p2"

class Game:
	def __init__(self):
		self.MessageBuilder = MessageBuilder(self)
		self._players = {}
		self._players[PLAYER1] = Paddle(Vec2(-0.9, 0.))
		self._players[PLAYER2] = Paddle(Vec2(0.9, 0.))
		self._ball = Ball(Vec2(1., 0.))
		self._score = [0, 0]

	# Players
	def RegisterKeyInput(self, current_player, key):
		self._players[current_player].key = key
		self._players[current_player].key_has_changed = True

	def UpdatePaddlePosition(self, current_player, delta_time):
		key = self._players[current_player].key
		if (key == DATA_INPUT_KEY_NONE):
			return

		move = self._players[current_player].speed * delta_time

		if (key == DATA_INPUT_KEY_DOWN):
			move *= -1.0

		self._players[current_player].position.y += move

	def UpdateBallPosition(self, delta_time):
		current_speed = (self._ball.speed + self._ball.acceleration) * delta_time

		delta_position = Vec2( 
			self._ball.direction.x * current_speed,
			self._ball.direction.y * current_speed
		)	

		self._ball.position.x += delta_position.x
		self._ball.position.y += delta_position.y
