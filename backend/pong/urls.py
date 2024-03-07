from django.urls import path
from . import views

app_name="pong"
urlpatterns = [
	path("play/", views.index, name="index"),
	path("game_list/", views.game_list, name="game_list")
]