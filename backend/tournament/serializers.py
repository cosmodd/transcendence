from rest_framework import serializers
from .models import Tournament

class FillTournamentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Tournament
        fields = ['id']

    def create(self, validated_data):
        tournament = Tournament.objects.FillTournament(
			id=validated_data['id'],
            user=self.context['request'].user
        )
        return tournament

class CreateTournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ['name', 'size']

    def create(self, validated_data):
        tournament = Tournament.objects.CreateTournament(
            name=validated_data['name'], 
			size=validated_data['size'],
            user=self.context['request'].user
        )
        return tournament