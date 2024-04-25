from django.urls import path
from .views import FillTournamentView

urlpatterns = [
	path("tournament/add/", FillTournamentView.as_view(), name='fill-tournament')
]