from django.urls import path
from .views import UserGameList

urlpatterns = [
	path("pong/<str:username>/", UserGameList.as_view(), name="games-by-username")
]