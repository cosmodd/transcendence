import json
from classes_objects import Ball, Paddle
from class_messagebuilder import MessageBuilder
from class_collision import Collision
from constants import *
from datetime import datetime
from class_vec2 import Vec2

__all__ = ["PLAYER1", "PLAYER2", "Game"]

PLAYER1, PLAYER2 = DATA_PLAYER_PLAYER1, DATA_PLAYER_PLAYER2

class Game:
	def __init__(self):
		self.MessageBuilder = MessageBuilder(self)
		self.Collision = Collision(self)
		self.players = {}
		self.players[PLAYER1] = Paddle(Vec2(-0.9, 0.))
		self.players[PLAYER2] = Paddle(Vec2(0.9, 0.))
		self.ball = Ball(Vec2(1., 0.))
		self.score = {}
		self.score[PLAYER1] = 0
		self.score[PLAYER2] = 0
		self.someone_scored = False

	# Players
	def RegisterKeyInput(self, current_player, key):
		self.players[current_player].key = key
		self.players[current_player].key_has_changed = True

	def UpdatePaddlePosition(self, current_player, delta_time):
		key = self.players[current_player].key
		if (key == DATA_INPUT_KEY_NONE):
			return

		move = self.players[current_player].speed * delta_time

		if (key == DATA_INPUT_KEY_DOWN):
			move *= -1.0

		self.players[current_player].position.y += move

	def UpdateBallPosition(self, delta_time):
		current_speed = (self.ball.speed + self.ball.acceleration) * delta_time

		delta_position = Vec2( 
			self.ball.direction.x * current_speed,
			self.ball.direction.y * current_speed
		)	

		self.ball.position.x += delta_position.x
		self.ball.position.y += delta_position.y
	
	def UpdateScore(self, player: str):
		self.score[player] += 1
		self.someone_scored = True
