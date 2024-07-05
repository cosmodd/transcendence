from django.db import models
from users.models import Account
from pong.models import Game

class TournamentManager(models.Manager):

	def CreateTournament(self, name, size, user):
		# User already signed somewhere
		if user.active_tournaments.exists():
			raise ValueError("An user is already signed in a tournament.")

		tournament = Tournament.objects.create(name=name, size=size)
		tournament.active_players.add(user)

		tournament.save()
		return tournament

	def JoinTournament(self, id, user, display_name):
		# User already in a game
		if user.games.filter(status='in_progress').exists():	
			raise ValueError("You are already in a game lobby.")
		
		# User already signed somewhere
		if user.active_tournaments.exists():
			raise ValueError("An user is already signed in a tournament.")
		
		# Existing tournament
		tournament = self.get(id=id)
		if (tournament.is_full):
			raise ValueError("Tournament is full")

		# Existing display name
		if tournament.active_players.filter(display_name=display_name).exists():
			raise ValueError("An user already has this display name.")
		user.display_name = display_name
		user.save()

		tournament.active_players.add(user)

		if (tournament.active_players.count() >= tournament.size):
			tournament.is_full = True
			tournament.status = 'in_progress'

		tournament.save()
		return tournament

class Tournament(models.Model):

	class Statuses(models.TextChoices):
		LOOKING_FOR_PLAYERS = 'looking_for_players', 'Looking for players'
		IN_PROGRESS = 'in_progress', 'In progress'
		OVER = 'over', 'Over'
		CANCELLED = 'cancelled', 'Cancelled'

	class Sizes(models.IntegerChoices):
		FOUR = 4
		EIGHT = 8

	name = models.CharField(max_length=100)
	size = models.IntegerField(choices=Sizes.choices, default=Sizes.FOUR)
	is_full = models.BooleanField(default=False)	
	active_players = models.ManyToManyField(Account, related_name='active_tournaments') # 1 max
	past_players = models.ManyToManyField(Account, related_name='past_tournaments')
	games = models.ManyToManyField(Game, related_name='tournament')
	status = models.CharField(max_length=20, choices=Statuses.choices, default=Statuses.LOOKING_FOR_PLAYERS)
	winner = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='won_tournaments')

	objects = TournamentManager()