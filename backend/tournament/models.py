from django.db import models
from users.models import Account
from pong.models import Game

class Tournament(models.Model):
	STATUS_CHOICES = (
		('in_progress', 'In progress'),
		('over', 'Over'),
		('canceled', 'Canceled')
	)

	name = models.CharField(max_length=100)
	active_players = models.ManyToManyField(Account, related_name='active_tournaments') # 1 max
	past_players = models.ManyToManyField(Account, related_name='past_tournaments')
	games = models.ManyToManyField(Game, related_name='tournament')
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
	winner = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='won_tournaments')

	def CreateTournament(self, name, usernames):
		if len(usernames) not in [4, 8]:
			raise ValueError("The number of players must be 4, or 8.") 
		if not name:
			raise ValueError("Tournament must have a name.")
		
		users = Account.objects.filter(username__in=usernames)
		for user in users:
			if user.active_tournaments.exists():
				raise ValueError("An user is already signed in a tournament.")
		
		tournament = Tournament.objects.create(name=name)
		tournament.active_players.add(*users)

		return tournament

		
		
		
