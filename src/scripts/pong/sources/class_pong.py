import json
from classes_objects import Ball, Paddle
from class_messagebuilder import MessageBuilder
from constants import *
from datetime import datetime

__all__ = ["PLAYER1", "PLAYER2", "Pong"]

PLAYER1, PLAYER2 = "p1", "p2"

class Pong:
	def __init__(self):
		self.MessageBuilder = MessageBuilder(self)
		self._players = {}
		self._players[PLAYER1] = Paddle([-0.9, 0.])
		self._players[PLAYER2] = Paddle([-0.9, 0.])
		self._ball = Ball([1., 0.])
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

		self._players[current_player].position[1] += move

	def UpdateBallPosition(self, delta_time):
		current_speed = (self._ball.speed + self._ball.acceleration) * delta_time

		delta_position = [
			self._ball.direction[0] * current_speed,
			self._ball.direction[1] * current_speed
		]

		self._ball.position[0] += delta_position[0]
		self._ball.position[1] += delta_position[1]
