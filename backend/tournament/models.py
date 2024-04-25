from django.db import models
from users.models import Account
from pong.models import Game

class TournamentManager(models.Manager):
	def FillTournament(self, name, size, username):
		if not name:
			raise ValueError("Tournament must have a name.")
		if not username:
			raise ValueError("User must have a name.")

		user = Account.objects.get(username=username)
		if user.active_tournaments.exists():
			raise ValueError("An user is already signed in a tournament.")
		
		tournament = None
		# Existing tournament
		if self.filter(name=name).exists():
			tournament = self.filter(name=name).first()
			if (tournament.is_full):
				raise ValueError("Tournament is full")
		# New tournament
		else:
			tournament = Tournament.objects.create(name=name, size=size)

		tournament.active_players.add(user)

		if (tournament.size == 'four') and tournament.active_players.count() >= 4:
				tournament.is_full = True
		if (tournament.size == 'height') and tournament.active_players.count() >= 8:
				tournament.is_full = True

		tournament.save()

		return tournament

class Tournament(models.Model):
	STATUS_CHOICES = (
		('looking_for_players', 'Looking for players'),
		('in_progress', 'In progress'),
		('over', 'Over'),
		('canceled', 'Canceled')
	)
	SIZE_CHOICES = (
		('four', 'Four'),
		('height', 'Height')
	)

	name = models.CharField(max_length=100)
	size = models.CharField(max_length=10, choices=SIZE_CHOICES, default='four')
	is_full = models.BooleanField(default=False)	
	active_players = models.ManyToManyField(Account, related_name='active_tournaments') # 1 max
	past_players = models.ManyToManyField(Account, related_name='past_tournaments')
	games = models.ManyToManyField(Game, related_name='tournament')
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='looking_for_players')
	winner = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='won_tournaments')

	objects = TournamentManager()