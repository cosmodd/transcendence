from rest_framework import serializers
from .models import Tournament

class FillTournamentSerializer(serializers.ModelSerializer):
    active_player = serializers.CharField(write_only=True)
    id = serializers.IntegerField()

    class Meta:
        model = Tournament
        fields = ['id', 'name', 'active_player']

    def create(self, validated_data):
        tournament = Tournament.objects.FillTournament(
			id=validated_data['id'],
            name=validated_data['name'], 
            username=validated_data['active_player']
        )
        return tournament

class CreateTournamentSerializer(serializers.ModelSerializer):
    active_player = serializers.CharField(write_only=True)

    class Meta:
        model = Tournament
        fields = ['name', 'size', 'active_player']

    def create(self, validated_data):
        tournament = Tournament.objects.CreateTournament(
            name=validated_data['name'], 
			size=validated_data['size'],
            username=validated_data['active_player']
        )
        return tournament