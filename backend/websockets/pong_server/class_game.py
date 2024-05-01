import asyncio
from constants import *
from classes_objects import Ball, Paddle
from class_messagebuilder import MessageBuilder
from class_collision import Collision
from class_vec2 import Vec2
from pong.models import Game as GameModel 
from pong.models import Score as ScoreModel
from users.models import Account as AccountModel
from class_tournament import ROUND_QUARTER, ROUND_SEMI, ROUND_FINAL
from asgiref.sync import sync_to_async
import sys

__all__ = ["PLAYER1", "PLAYER2", "Game"]

PLAYER1, PLAYER2 = DATA_PLAYER_PLAYER1, DATA_PLAYER_PLAYER2

class Game:
	def __init__(self, room_id, clients, tournament = None):
		self.InitClients(clients)
		self.InitAttachedTournament(tournament)
		self.MessageBuilder = MessageBuilder(self)
		self.Collision = Collision(self)
		self.players = {}
		self.players[PLAYER1] = Paddle(Vec2(-0.9, 0.))
		self.players[PLAYER2] = Paddle(Vec2(0.9, 0.))
		self.ball = Ball(Vec2(1., 0.))
		self.score = {}
		self.model = {}
		self.start_time = 0
		self.room_id = room_id
		self.reconnection_lock = asyncio.Lock()
		self.winner = ""
		self.pause_timer = 0
		self.pause_time_added = 0
		self.game_ended_with_timeout = False
		self.match_is_running = True
		self.match_is_paused = False
		self.someone_scored = False
		self.canceled = False

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
	
	def StopBall(self):
		self.ball.direction = Vec2(0.0, 0.0)
	
	async def UpdateScore(self, player: str):
		self.score[player].score += 1
		await self.score[player].asave()
		self.someone_scored = True

	def IsMatchRunning(self):
		return self.match_is_running

	def IsMatchPaused(self):
		return self.match_is_paused

	async def ClientsAreReady(self):
		if (await self.clients[0].IsReady() == True and await self.clients[1].IsReady() == True):
				return True
		return False
	
	def OpponentUsernameOf(self, username: str):
		return self.clients[0].username if username != self.clients[0].username else self.clients[1].username

	def InitClients(self, clients):
		self.clients = clients
		self.connected = []
		self.disconnected = []
		for client in clients:
			if client.ws == None or client.ws.closed:
				sys.stderr.write("DEBUG::" + client.username + " added to disconnected\n")
				self.disconnected.append(client)
			else:
				sys.stderr.write("DEBUG::" + client.username + " added to connected\n")
				self.connected.append(client)

	def InitAttachedTournament(self, tournament):
		self.attached_tournament = tournament
		if (self.attached_tournament == None):
			return
		self.attached_tournament.games.append(self)

	async def CreateModel(self, game_type: str):
		self.model = await GameModel.objects.acreate(room_id=self.room_id)
		account_list = [await AccountModel.objects.aget(username=self.clients[0].username), await AccountModel.objects.aget(username=self.clients[1].username)]
		await self.model.players.aadd(*account_list)
		self.model.type = game_type

		# Tournament stuff
		if self.attached_tournament != None:
			self.model.round = self.attached_tournament.round
			await self.attached_tournament.model.games.aadd(self.model)

		await self.model.asave()
		self.score[PLAYER1] = await ScoreModel.objects.acreate(game=self.model, score=0)
		self.score[PLAYER2] = await ScoreModel.objects.acreate(game=self.model, score=0)
		await self.score[PLAYER1].asave()
		await self.score[PLAYER2].asave()

	async def TerminateModel(self):
		if (self.canceled):
			self.model.status = 'canceled'
			await self.model.asave()
			return

		if (self.game_ended_with_timeout):
			self.winner = self.connected[0].username
		else:
			self.winner = self.clients[0].username if (self.score[PLAYER1].score >= self.score[PLAYER2].score) else self.clients[1].username
		self.model.status = 'over'
		self.model.ended_with_timeout = self.game_ended_with_timeout
		self.model.winner = await AccountModel.objects.aget(username=self.winner)
		await self.model.asave()

		if (self.model.type == DATA_LOBBY_GAME_TYPE_TOURNAMENT):
			loser = self.clients[0] if (self.score[PLAYER1].score < self.score[PLAYER2].score) else self.clients[1]
			await self.attached_tournament.RemoveClient(loser)