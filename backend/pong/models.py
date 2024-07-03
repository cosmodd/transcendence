from django.db import models
from users.models import Account

class Game(models.Model):
	STATUS_CHOICES = (
		('in_progress', 'In progress'),
		('over', 'Over'),
		('cancelled', 'Cancelled'),
	)
	TYPE_CHOICES = (
		('duel', 'Duel'),
		('tournament', 'Tournament'),
	)
	ROUND_CHOICES = (
		('none', 'None'),
		('quarter', 'Quarter Final'),
		('semi', 'Semi Final'),
		('final', 'Final'),
	) 

	players = models.ManyToManyField(Account, related_name='games')
	date_begin = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
	winner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='games_won', null=True, blank=True)
	ended_with_timeout = models.BooleanField(default=False)
	room_id = models.CharField(max_length=5, null=True)
	type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='duel')
	round = models.CharField(max_length=20, choices=ROUND_CHOICES, null=True)

	def __str__(self):
		scores = self.scores.all()
		scores_str = ' - '.join([f"{score.score}" for score in scores])
		winner_username = self.winner.username if self.winner else None
		return f"Partie ({self.id}), {self.status}, Room_ID: {self.room_id}, {scores_str}, Winner: {winner_username}"
	
	def tournament_output(self) -> dict:
		players = [
			{
				"username": player.username,
				"display_name": player.display_name,
				"profile_image": player.get_profile_image_url()
			}
			for player in self.players.all()
		]
		scores = [score.score for score in self.scores.all()]
		return {
			"players": players,
			"type": self.type,
			"round": self.round,
			"status": self.status,
			"scores": scores,
			"winner": self.winner.username if self.winner else None,
			"timeout": self.ended_with_timeout,
			"date_begin": self.date_begin
		}

	class Meta:
		verbose_name = "Game"
		verbose_name_plural = "Games"

class Score(models.Model):
	# player = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="scores")
	game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="scores", null=False)
	score = models.IntegerField(null=False)

	def __str__(self):
		return f"{self.score}"

