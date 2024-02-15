from django.urls import path
from . import views

app_name="pong"
urlpatterns = [
	path("", views.game_list, name="game_list"),
]