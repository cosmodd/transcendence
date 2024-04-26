from django.urls import path
from .views import FillTournamentView, CreateTournamentView

urlpatterns = [
	path("tournament/fill/", FillTournamentView.as_view(), name='fill-tournament'),
	path("tournament/create/", CreateTournamentView.as_view(), name='create-tournament')
]