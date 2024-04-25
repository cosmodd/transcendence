from rest_framework import serializers
from .models import Tournament

class TournamentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tournament
		fields = ['name', 'active_players']

	def create(self, validated_data):
		tournament = Tournament.objects.CreateTournament(
			name=validated_data['name'], 
			usernames=validated_data['active_players']
		)
		return tournament