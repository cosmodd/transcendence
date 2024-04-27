import asyncio
from tournament.models import Tournament as TournamentModel
from users.models import Account as AccountModel
from class_client import Client
import sys
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

async def IsUserActiveInTournament(username) -> bool:
	tournament = await TournamentModel.objects.filter(active_players__username=username).aget()
	return tournament is not None

class Tournament:
	async def Init(self, original_client: Client):
		# Find model in database
		self.model = await TournamentModel.objects.filter(active_players__username=original_client.username).aget()
		sys.stderr.write("DEBUG:: TournamentModel found\n")
		self.round = self.InitRound()
		sys.stderr.write("DEBUG:: Tournament round :" + str(self.round) + "\n")
		self.clients = await self.InitClients(original_client)
		sys.stderr.write("DEBUG:: Tournament clients created\n")
		self.games = []
		self.LaunchGamesForRound()


	def InitRound(self):
		if (self.model.size == 'eight'):
			return ROUND_QUARTER
		return ROUND_SEMI

	async def InitClients(self, original_client):
		clients = []
		users = []
		try:
			users = await sync_to_async(list)(self.model.active_players.all())
		except Exception as e:
			print("Une erreur s'est produite :", e)

		sys.stderr.write("DEBUG:: after retrieve\n")
		for user in users:
			# User that initiated the tournament creation
			sys.stderr.write("DEBUG:: in loop\n")
			if user.username == original_client.username:
				clients.append(original_client)
			else:
				clients.append(Client(None, user.username))
		return clients

	async def RemoveClient(self, loser):
		for client in self.clients:
			if client.username == loser.username:
				self.clients.remove(client)
		to_remove = await self.model.active_players.aget(username=loser.username)
		self.model.active_players.remove(to_remove)
		self.model.past_players.add(to_remove)
	
	def LaunchGamesForRound(self):
		from handler import NewRoom
		from class_game import PLAYER1, PLAYER2

		games_count = ROUNDS_TO_COUNT[self.round]

		for i in range(games_count):
			client1 = self.clients[i*2]
			client1.name = PLAYER1
			client2 = self.clients[i*2+1]
			client2.name = PLAYER2
			asyncio.create_task(NewRoom([client1, client2], DATA_LOBBY_GAME_TYPE_TOURNAMENT, self))

		sys.stderr.write("DEBUG:: Tournament games launched for round : " + str(self.round))
	
	async def LaunchNextRoundIfNecessary(self):
		current_round_ended_games = await self.model.games.filter(status='over', round=self.round).count()
		if (current_round_ended_games != ROUNDS_TO_COUNT[self.round]):
			return
		
		self.round += 1
		if (self.round not in ROUNDS):
			sys.stderr.write("DEBUG:: Tournament over, terminating model")
			#self.TerminateModel()
			return
		
		self.LaunchGamesForRound()



