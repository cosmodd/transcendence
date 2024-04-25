from django.urls import path
from .views import UserGameList

urlpatterns = [
	path("game/<str:username>/", UserGameList.as_view(), name="games-by-username")
]