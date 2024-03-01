import json
import datetime
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
				self.attached_game.score[DATA_PLAYER_PLAYER1].score,
				self.attached_game.score[DATA_PLAYER_PLAYER2].score
			], 
			DATA_TIME: (datetime.datetime.now() - self.attached_game.start_time).total_seconds()
		})
	
	def PausedGame(self):
		return json.dumps({
			METHOD: FROM_SERVER,
			OBJECT: OBJECT_LOBBY,
			DATA_LOBBY_STATE: DATA_LOBBY_ROOM_PAUSED,
			DATA_INFO_TYPE: DATA_INFO_TYPE_MESSAGE,
			DATA_INFO_TYPE_MESSAGE: "Match paused."
		})

	def Reconnection(self):
		return json.dumps({
			METHOD: FROM_SERVER,
			OBJECT: OBJECT_LOBBY,
			DATA_LOBBY_STATE: DATA_LOBBY_ROOM_RECONNECTED,
			DATA_INFO_TYPE: DATA_INFO_TYPE_MESSAGE,
			DATA_INFO_TYPE_MESSAGE: "Reconnection..."
		})
	
	def OpponentReconnected(self):
		return json.dumps({
			METHOD: FROM_SERVER,
			OBJECT: OBJECT_LOBBY,
			DATA_LOBBY_STATE: DATA_LOBBY_ROOM_RECONNECTED,
			DATA_INFO_TYPE: DATA_INFO_TYPE_MESSAGE,
			DATA_INFO_TYPE_MESSAGE: "Opponent Reconnected."
		})


	
	def EndGame(self):
		return json.dumps({
			METHOD: FROM_SERVER,
			OBJECT: OBJECT_LOBBY,
			DATA_LOBBY_STATE: DATA_LOBBY_ROOM_ENDED,
			DATA_INFO_TYPE: DATA_INFO_TYPE_MESSAGE,
			DATA_INFO_TYPE_MESSAGE: self.attached_game.winner + " won."
		})

