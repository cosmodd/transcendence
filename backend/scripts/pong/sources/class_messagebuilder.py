import json
from constants import *
from class_vec2 import Vec2
from class_game import *

class MessageBuilder:
	def __init__(self, game):
		self.attached_game = game

	def Paddle(self, player):
		position = self.attached_game.players[player].position
		key = self.attached_game.players[player].key
		return json.dumps({
                    METHOD: FROM_SERVER,
                    OBJECT: OBJECT_PADDLE,
					DATA_PLAYER: player,
                    DATA_POSITION: [position.x, position.y],
                    DATA_INPUT: key
                })

	def Ball(self):
		position = self.attached_game.ball.position
		direction = self.attached_game.ball.direction
		acceleration = self.attached_game.ball.acceleration
		return json.dumps({
                    METHOD: FROM_SERVER,
                    OBJECT: OBJECT_BALL,
                    DATA_POSITION: [position.x, position.y],
                    DATA_DIRECTION: [direction.x, direction.y],
                    DATA_ACCELERATION: acceleration
                })
	
	def Score(self):
		return json.dumps({
			METHOD: FROM_SERVER,
			OBJECT: OBJECT_LOBBY,
			DATA_LOBBY_SCORE: [
				self.attached_game.score[DATA_PLAYER_PLAYER1],
				self.attached_game.score[DATA_PLAYER_PLAYER2]
			] 
		})