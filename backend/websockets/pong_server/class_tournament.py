import asyncio
from tournament.models import Tournament as TournamentModel
from users.models import Account as AccountModel
from class_client import Client
from constants import *
import sys
import traceback
from asgiref.sync import async_to_sync

ROUND_QUARTER = "quarter"
ROUND_SEMI = "semi"
ROUND_FINAL = "final"

ROUNDS_TO_COUNT = {
	ROUND_QUARTER: 4,
	ROUND_SEMI: 2,
	ROUND_FINAL: 1
}

ROUNDS = {
	ROUND_QUARTER: ROUND_QUARTER,
	ROUND_SEMI: ROUND_SEMI,
	ROUND_FINAL: ROUND_FINAL
}

async def TournamentNeedsToBeCreated(username) -> bool:
	tournament = await TournamentModel.objects.filter(active_players__username=username).aget()
	active_players_count = 0
	async for user in AccountModel.objects.filter(active_tournaments__id=tournament.id).all():
		active_players_count += 1
	
	if (active_players_count == 8 and tournament.size == 'eight'):
		return True
	if (active_players_count == 4 and tournament.size == 'four'):
		return True
	return False	

async def IsUserActiveInTournament(username) -> bool:
	try:
		tournament = await TournamentModel.objects.filter(active_players__username=username).aget()
		return tournament is not None
	except:
		return False

class Tournament:
	async def Init(self, original_client: Client):
		# Find model in database
		self.model = await TournamentModel.objects.filter(active_players__username=original_client.username).aget()
		sys.stderr.write("DEBUG:: TournamentModel found : " + str(self.model.name) + "\n")
		self.round = self.InitRound()
		sys.stderr.write("DEBUG:: Tournament round :" + str(self.round) + "\n")
		self.clients = await self.InitClients(original_client)
		sys.stderr.write("DEBUG:: Tournament clients created\n")
		self.games = []
		self.rooms_tasks = set()

	def InitRound(self):
		if (self.model.size == 'eight'):
			return ROUND_QUARTER
		return ROUND_SEMI

	async def InitClients(self, original_client):
		clients = []

		async for user in AccountModel.objects.filter(active_tournaments__id=self.model.id).all():
			# User that initiated the tournament creation
			sys.stderr.write(str(user.username) + "\n")
			if user.username == original_client.username:
				clients.append(original_client)
			else:
				clients.append(Client(None, str(user.username)))
		
		return clients

	async def RemoveClient(self, loser):
		for client in self.clients:
			if client.username == loser.username:
				self.clients.remove(client)
		to_remove = await self.model.active_players.aget(username=loser.username)
		await self.model.active_players.aremove(to_remove)
		await self.model.past_players.aadd(to_remove)
	
	async def IsLaunchingNextRoundNecessary(self):
		current_round_ended_games = 0 
		async for i in self.model.games.filter(status='over', round=self.round).all():
			current_round_ended_games += 1
		return (current_round_ended_games == ROUNDS_TO_COUNT[self.round])

	async def LaunchNextRoundIfNecessary(self):
		current_round_ended_games = 0 
		async for i in self.model.games.filter(status='over', round=self.round).all():
			current_round_ended_games += 1
		if (current_round_ended_games != ROUNDS_TO_COUNT[self.round]):
			return
		
		self.round += 1
		if (self.round not in ROUNDS):
			sys.stderr.write("DEBUG:: Tournament over, terminating model")
			#self.TerminateModel()
			return


		


