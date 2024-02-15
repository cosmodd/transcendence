from django.http import JsonResponse
from .models import Game, Score

def game_list(request):
	games = Game.objects.all()
	data = []

	for game in games:
		scores = Score.objects.filter(game=game)
		scores_data = [{'player': "unspecified",'score': score.score} for score in scores], 
		game_data = {
			'id': game.id,
			'status': game.status,
			'scores': scores_data,
			'date': game.date_begin
		}
		data.append(game_data)

	return JsonResponse(data, safe=False)