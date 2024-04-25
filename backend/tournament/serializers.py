from rest_framework import serializers
from .models import Tournament

class TournamentSerializer(serializers.ModelSerializer):
    active_player = serializers.CharField(write_only=True)

    class Meta:
        model = Tournament
        fields = ['name', 'size', 'active_player']

    def create(self, validated_data):
        tournament = Tournament.objects.FillTournament(
            name=validated_data['name'], 
			size=validated_data['size'],
            username=validated_data['active_player']
        )
        return tournament