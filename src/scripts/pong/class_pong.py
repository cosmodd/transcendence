import json
from classes_objects import Ball, Paddle
from class_messagebuilder import MessageBuilder

__all__ = ["PLAYER1", "PLAYER2", "Pong"]

PLAYER1, PLAYER2 = "p1", "p2"

class Pong:
	def __init__(self):
		self.MessageBuilder = MessageBuilder(self)
		self._players = {}
		self._players[PLAYER1] = Paddle([0., 0.])
		self._players[PLAYER2] = Paddle([0., 0.])
		#self._ball = Ball()
		self._score = [0, 0]

	# Players
	def ActualizePlayerPosition(self, current_player, new_position):
		# assert some rules

		#replace player position
		self._players[current_player].position = new_position	

	def GetPlayerPosition(self, current_player):
		return self._players[current_player].position
