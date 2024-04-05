from django.http import JsonResponse
from django.shortcuts import render
from .models import Game, Score
from users.models import Account
from users.serializers import ProfileSerializer
from rest_framework import generics
from rest_framework.response import Response

def index(request):
	return render(request, "pong/index.html")

class UserGameList(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'username'

    def get_object(self):
        return Account.objects.get(username=self.kwargs['username'])

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        games = Game.objects.filter(players=user)
        games_list = []
        for game in games:
            players_names = [player.username for player in game.players.all()]
            scores = game.scores.all()
            scores_str = [score.score for score in scores]
            games_list.append(
                {
					"players": players_names,
                    "type": game.type,
                    "status": game.status,
                    "scores": scores_str,
                    # "winner": game.winner.username,
                    "date_begin": game.date_begin
                }
            )
        return Response({"games": games_list})