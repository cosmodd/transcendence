from django.urls import path
from .views import RegisterView, LoginView, ProfileView, AuthentificationWith42View, Handle42CallbackView, UserProfile, UpdateProfileView, Check_two_factor_code
from rest_framework_simplejwt.views import TokenRefreshView
import sys

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),


    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', ProfileView.as_view(), name='user'),
    path('user/<str:username>/', UserProfile.as_view(), name='user-by-username'),

    path('auth/42/', AuthentificationWith42View.as_view(), name='authentification-with-42'),
    path('auth/42/callback/', Handle42CallbackView.as_view(), name='authentification-with-42-callback'),
    
    # TODO : clean this
    path('profile/update/', UpdateProfileView.as_view(), name='update-profile'),
    path('fa/', Check_two_factor_code.as_view(), name='2fa'),
]