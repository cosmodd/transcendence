from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .serializers import CreateTournamentSerializer, JoinTournamentSerializer
from .models import Tournament
import traceback

class JoinTournamentView(generics.CreateAPIView):
	serializer_class = JoinTournamentSerializer
	permission_classes = [permissions.IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)

		try:
			if serializer.is_valid():
				serializer.save()
				return Response({
					"id": request.data['id']
				}, status=status.HTTP_201_CREATED)
			else:
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			traceback.print_exc()
			return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CreateTournamentView(generics.CreateAPIView):
	serializer_class = CreateTournamentSerializer
	permission_classes = [permissions.IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)

		try:
			if serializer.is_valid():
				tournament = serializer.save()
				return Response({
					"id": tournament.id,
					"name": tournament.name,
					"size": tournament.size
				}, status=status.HTTP_201_CREATED)
			else:
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			traceback.print_exc()
			return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ActiveTournamentsListView(generics.RetrieveAPIView):
	permission_classes = [permissions.IsAuthenticated]

	def get(self, request, *args, **kwargs):
		tournaments = Tournament.objects.filter(status__in=['in_progress', 'looking_for_players'])
		tournaments_list = []
		for t in tournaments:
			tournaments_list.append(
				{
					'name': t.name,
					'id': t.id,
					'status': t.status,
					'players_count' : t.active_players.count() + t.past_players.count(),
					'size': t.size,
					'players': [user.username for user in t.active_players.all()] + [user.username for user in t.past_players.all()]
				}
			)
		return Response(tournaments_list)

class SpecificTournamentView(generics.RetrieveAPIView):
	permission_classes = [permissions.IsAuthenticated]

	def get_object(self):
		return Tournament.objects.get(id=self.kwargs['pk'])

	def get(self, request, *args, **kwargs):
		tournament = self.get_object()
		return Response({
			'name': tournament.name,
			'id': tournament.id,
			'status': tournament.status,
			'winner': tournament.winner.username if tournament.winner else tournament.winner,
			'size': tournament.size,
			'active_players': [user.username for user in tournament.active_players.all()],
			'past_players': [user.username for user in tournament.past_players.all()],
			'games': [game.tournament_output() for game in tournament.games.all()]
		})