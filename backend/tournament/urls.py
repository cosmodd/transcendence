from django.urls import path
from .views import *

urlpatterns = [
	path("tournament/join/", FillTournamentView.as_view(), name='fill-tournament'),
	path("tournament/create/", CreateTournamentView.as_view(), name='create-tournament'),
	path("tournament/", ActiveTournamentsListView.as_view(), name='list-tournaments'),
	path("tournament/<str:pk>/", SpecificTournamentView.as_view(), name='get-tournament')
]