from django.urls import path
from .views import RegisterView, LoginView, ProfileView, UpdateProfileView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    # path('profile/update/', UpdateProfileView.as_view(), name='update-profile'), TODO: build this view
]