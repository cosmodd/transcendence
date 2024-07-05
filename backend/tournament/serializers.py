from rest_framework import serializers
from .models import Tournament

class JoinTournamentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    display_name = serializers.CharField(max_length=255)

    class Meta:
        model = Tournament
        fields = ['id', 'display_name']

    def create(self, validated_data):
        tournament = Tournament.objects.JoinTournament(
			id=validated_data['id'],
            display_name = validated_data['display_name'],
            user=self.context['request'].user,
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