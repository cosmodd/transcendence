import sys
from django.http import JsonResponse
from django.shortcuts import render
from .models import Game, Score
from users.models import Account
from users.serializers import ProfileSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
import traceback

def index(request):
	return render(request, "pong/index.html")

class UserGameList(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'username'

    def get_object(self):
        return Account.objects.get(username=self.kwargs['username'])

    def get(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            games = Game.objects.filter(players=user).order_by('date_begin')
            games_list = []
            for game in games:
                if game.status != 'over':
                    continue

                players_names = [{
                     "username": player.username,
                     "display_name": player.display_name
                } for player in game.players.all()]
                scores = game.scores.all()
                scores_str = [score.score for score in scores]
                games_list.append(
                    {
                        "players": players_names,
                        "type": game.type,
                        "status": game.status,
                        "scores": scores_str,
                        "winner": game.winner.username if game.winner else None,
                        "timeout": game.ended_with_timeout,
                        "date_begin": game.date_begin,
                        "round": game.round,
                        "tournament": game.tournament.first().id if game.type == 'tournament' else None
                    }
                )
            return Response({"games": games_list}, status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
