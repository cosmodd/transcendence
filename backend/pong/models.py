from django.db import models
from users.models import Account

class Game(models.Model):
	STATUS_CHOICES = (
			('en_attente', 'En attente'),
			('en_cours', 'En cours'),
			('terminee', 'Terminée'),
			('annulee', 'Annulée'),
		)

	players = models.ManyToManyField(Account, related_name='games')
	date_begin = models.DateTimeField(auto_now_add=True)
	duration = models.DurationField(null=True, blank=True)
	statut = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_attente')
	winner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='games_won', null=True, blank=True)

	def __str__(self):
		return f"Partie ({self.id}) - Début: {self.date_begin}, Statut: {self.statut}, Gagnant: {self.winner}"

	class Meta:
		verbose_name = "Game"
		verbose_name_plural = "Games"

class Score(models.Model):
	player = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="scores")
	game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="scores")
	score = models.IntegerField()

	def __str__(self):
		return f"Score de {self.player.username} dans la partie ({self.game.id}): {self.score}"

