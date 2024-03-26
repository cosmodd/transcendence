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
			DATA_ACCELERATION: acceleration,
			DATA_TIME: (datetime.datetime.now() - self.attached_game.start_time).total_seconds() - self.attached_game.pause_time_added
		})

	def FreezeBall(self):
		position = self.attached_game.ball.position
		direction = Vec2(0, 0)
		acceleration = 0
		return json.dumps({
			METHOD: FROM_SERVER,
			OBJECT: OBJECT_BALL,
			DATA_POSITION: [position.x, position.y],
			DATA_DIRECTION: [direction.x, direction.y],
			DATA_ACCELERATION: acceleration,
			DATA_TIME: (datetime.datetime.now() - self.attached_game.start_time).total_seconds() - self.attached_game.pause_time_added
		})
	
	def Score(self):
		return json.dumps({
			METHOD: FROM_SERVER,
			OBJECT: OBJECT_LOBBY,
			DATA_LOBBY_SCORE: [
				self.attached_game.score[DATA_PLAYER_PLAYER1].score,
				self.attached_game.score[DATA_PLAYER_PLAYER2].score
			], 
			DATA_TIME: (datetime.datetime.now() - self.attached_game.start_time).total_seconds() - self.attached_game.pause_time_added
		})
	
	def PausedGame(self):
		return json.dumps({
			METHOD: FROM_SERVER,
			OBJECT: OBJECT_LOBBY,
			DATA_LOBBY_STATE: DATA_LOBBY_ROOM_PAUSED,
			DATA_INFO_TYPE: DATA_INFO_TYPE_MESSAGE,
			DATA_INFO_TYPE_MESSAGE: "Match paused."
		})

	def Reconnection(self, client_ready_state):
		return json.dumps({
			METHOD: FROM_SERVER,
			OBJECT: OBJECT_LOBBY,
			DATA_LOBBY_STATE: DATA_LOBBY_ROOM_RECONNECTED,
			DATA_INFO_TYPE: DATA_INFO_TYPE_MESSAGE,
			DATA_INFO_TYPE_MESSAGE: "Reconnection...",
			DATA_PLAYER_STATE: DATA_PLAYER_READY if client_ready_state == True else DATA_PLAYER_NOT_READY,
			DATA_TIME: (datetime.datetime.now() - self.attached_game.start_time).total_seconds() - self.attached_game.pause_time_added if self.attached_game.ClientsAreReady() else 0
		})
	
	def OpponentReconnected(self):
		return json.dumps({
			METHOD: FROM_SERVER,
			OBJECT: OBJECT_LOBBY,
			DATA_LOBBY_STATE: DATA_LOBBY_ROOM_RECONNECTED,
			DATA_INFO_TYPE: DATA_INFO_TYPE_MESSAGE,
			DATA_INFO_TYPE_MESSAGE: "Opponent Reconnected.",
			DATA_TIME: (datetime.datetime.now() - self.attached_game.start_time).total_seconds() - self.attached_game.pause_time_added if self.attached_game.ClientsAreReady() else 0
		})
	
	def EndGame(self):
		return json.dumps({
			METHOD: FROM_SERVER,
			OBJECT: OBJECT_LOBBY,
			DATA_LOBBY_STATE: DATA_LOBBY_ROOM_ENDED,
			DATA_INFO_TYPE: DATA_INFO_TYPE_MESSAGE,
			DATA_INFO_TYPE_MESSAGE: ("Timeout. " if self.attached_game.game_ended_with_timeout else "") + self.attached_game.winner + " won."
		})

	def NewRoomInfoFor(self, client_index):
		return json.dumps({
            METHOD: FROM_SERVER,
            OBJECT: OBJECT_LOBBY,
            DATA_LOBBY_STATE: DATA_LOBBY_ROOM_CREATED,
            DATA_INFO_TYPE: DATA_INFO_TYPE_MESSAGE,
            DATA_INFO_TYPE_MESSAGE: "Room found: " + str(self.attached_game.room_id),
            DATA_LOBBY_ROOM_ID: self.attached_game.room_id,
            DATA_PLAYER: self.attached_game.connected[client_index].name,
            DATA_PLAYER_TOKEN: self.attached_game.connected[client_index].token
		})
	
	def ClientsAreReady(self, client_index):
		return json.dumps({
            METHOD: FROM_SERVER,
            OBJECT: OBJECT_LOBBY,
            DATA_LOBBY_STATE: DATA_PLAYER_READY,
            DATA_PLAYER: self.attached_game.connected[client_index].name,
            DATA_INFO_TYPE: DATA_INFO_TYPE_MESSAGE,
            DATA_INFO_TYPE_MESSAGE: "Game is on!"
		})

