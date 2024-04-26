import asyncio
from tournament.models import Tournament as TournamentModel
from class_game import PLAYER1, PLAYER2
from users.models import Account as AccountModel
from class_client import Client

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

def IsUserActiveInTournament(username) -> bool:
	tournament = TournamentModel.objects.filter(active_players__username=username)
	return tournament.exists()

class Tournament:
	def __init__(self, original_client: Client):
		# Find model in database
		self.model = TournamentModel.objects.filter(active_players__username=original_client.username)
		self.round = self.InitRound()
		self.clients = self.InitClients(original_client)
		self.games = []
		self.LaunchGamesForRound()
	
	def InitRound(self):
		if (self.model.size == 'eight'):
			return ROUND_QUARTER
		return ROUND_SEMI

	def InitClients(self, original_client):
		clients = []
		for user in self.model.active_players.all():
			# User that initiated the tournament creation
			if user.username == original_client.username:
				clients.append(original_client)
			else:
				clients.append(Client(None, user.username))
		return clients

	def RemoveClient(self, loser):
		for client in self.clients:
			if client.username == loser.username:
				self.clients.remove(client)
		to_remove = self.model.active_players.get(username=loser.username)
		self.model.active_players.remove(to_remove)
		self.model.past_players.add(to_remove)
	
	def LaunchGamesForRound(self):
		from handler import NewRoom

		games_count = ROUNDS_TO_COUNT[self.round]

		for i in range(games_count):
			client1 = self.clients[i*2]
			client1.name = PLAYER1
			client2 = self.clients[i*2+1]
			client2.name = PLAYER2
			asyncio.create_task(NewRoom([client1, client2], DATA_LOBBY_GAME_TYPE_TOURNAMENT, self))
	
	def LaunchNextRoundIfNecessary(self):
		current_round_ended_games = self.model.games.filter(status='over', round=self.round).count()
		if (current_round_ended_games != ROUNDS_TO_COUNT[self.round]):
			return
		
		self.round += 1
		if (self.round not in ROUNDS):
			sys.stderr.write("DEBUG:: Tournament over, terminating model")
			#self.TerminateModel()
			return
		
		self.LaunchGamesForRound()



