from django.urls import path
from .views import *

urlpatterns = [
	path("tournament/fill/", FillTournamentView.as_view(), name='fill-tournament'),
	path("tournament/create/", CreateTournamentView.as_view(), name='create-tournament'),
	path("tournament/list/", ActiveTournamentsListView.as_view(), name='list-tournaments'),
	path("tournament/get/<str:pk>/", SpecificTournamentView.as_view(), name='get-tournament')
]