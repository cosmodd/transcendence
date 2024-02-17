from constants import *
from classes_objects import Ball, Paddle
from class_messagebuilder import MessageBuilder
from class_collision import Collision
from class_vec2 import Vec2
from pong.models import Game as GameModel 
from pong.models import Score as ScoreModel
from asgiref.sync import sync_to_async

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
		# self.score[PLAYER1] = 0
		# self.score[PLAYER2] = 0
		self.someone_scored = False
		self.model = {}
		self.match_is_running = True

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
	
	async def UpdateScore(self, player: str):
		self.score[player].score += 1
		await self.score[player].asave()
		self.someone_scored = True

	def IsMatchRunning(self):
		return self.match_is_running

	async def CreateModel(self, room_id):
		self.model = await GameModel.objects.acreate(room_id=room_id)
		await self.model.asave()
		self.score[PLAYER1] = await ScoreModel.objects.acreate(game=self.model, score=0)
		self.score[PLAYER2] = await ScoreModel.objects.acreate(game=self.model, score=0)
		await self.score[PLAYER1].asave()
		await self.score[PLAYER2].asave()

	async def TerminateModel(self):
		self.model.status = 'terminee'
		await self.model.asave()
