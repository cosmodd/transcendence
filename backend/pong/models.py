from django.db import models
from users.models import Account

class Game(models.Model):
	STATUS_CHOICES = (
			('en_cours', 'En cours'),
			('terminee', 'Terminée'),
			('annulee', 'Annulée'),
	)

	players = models.ManyToManyField(Account, related_name='games')
	date_begin = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_cours')
	winner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='games_won', null=True, blank=True)
	room_id = models.CharField(max_length=5, null=True)
	#game_type (duel, tournament, casual, local)

	def __str__(self):
		scores = self.scores.all()
		scores_str = ' - '.join([f"{score.score}" for score in scores])
		return f"Partie ({self.id}), {self.status}, Room_ID: {self.room_id}, {scores_str}, Winner: {self.winner.username}"

	class Meta:
		verbose_name = "Game"
		verbose_name_plural = "Games"

class Score(models.Model):
	# player = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="scores")
	game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="scores", null=False)
	score = models.IntegerField(null=False)

	def __str__(self):
		return f"{self.score}"

