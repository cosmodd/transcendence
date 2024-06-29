from django.urls import path
from .views import RegisterView, LoginView, ProfileView, UserProfile, Handle42AuthView, RedirectTo42View, UserOnlineStatusView, UpdateProfileView, Check_two_factor_code
from rest_framework_simplejwt.views import TokenRefreshView
import sys

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', ProfileView.as_view(), name='user'),
    path('user/<str:username>/', UserProfile.as_view(), name='user-by-username'),

    path('auth/42/redirect/', RedirectTo42View.as_view(), name='authentification-with-42-redirect'),
    path('auth/42/', Handle42AuthView.as_view(), name='authentification-with-42'),
    path('user_status/<str:username>', UserOnlineStatusView.as_view(), name='user-status'),
    
    # TODO : clean this
    path('profile/update/', UpdateProfileView.as_view(), name='update-profile'),
    path('fa/', Check_two_factor_code.as_view(), name='2fa'),
]