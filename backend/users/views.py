from django.views.generic import RedirectView, View
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, parsers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import UntypedToken
from .models import Account
from .serializers import AccountSerializer, ProfileSerializer, LoginSerializer, UpdateProfileSerializer, UserOnlineSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import re, requests, random, string, os, sys
from django.http import JsonResponse
from datetime import datetime
from friend.models import OnlineStatus

# *******************************************************************************************************************
# ************************************************* Register / Login ************************************************
# *******************************************************************************************************************

class RegisterView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        # check if required fields are present
        if not request.data['username']:
            return Response({"message": "Username is required"}, status=401)
        if not request.data['email']:
            return Response({"message": "Email is required"}, status=401)
        if not request.data['password']:
            return Response({"message": "Password is required"}, status=401)

        # check if username and email already exists
        if Account.objects.filter(username=request.data['username']).exists():
            return Response({"message": "Username already exists"}, status=401)
        if Account.objects.filter(email=request.data['email']).exists():
            return Response({"message": "Email already exists"}, status=401)

        # length of username should be between 2 and 32 characters
        if len(request.data['username']) < 2 or len(request.data['username']) > 32:
            return Response({"message": "Username must be between 2 and 32 characters long"}, status=401)
        # username should contain only letters, numbers, underscores and dots
        if not re.match("^[a-z0-9_.]*$", request.data['username']):
            return Response({"message": "Username can only contain lowercase letters, numbers, underscores and dots"}, status=401)
        # not allow consecutive dots or underscores
        if ".." in request.data['username'] or "__" in request.data['username']:
            return Response({"message": "Username can't have consecutive dots or underscores"}, status=401)
        if request.data['username'][0] == '.' or request.data['username'][0] == '_':
            return Response({"message": "Username can't start with a dot or an underscore"}, status=401)
        if request.data['username'][-1] == '.' or request.data['username'][-1] == '_':
            return Response({"message": "Username can't end with a dot or an underscore"}, status=401)
        # email should be valid format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", request.data['email']):
            return Response({"message": "Invalid email"}, status=401)
        if len(request.data['password']) < 8:
            return Response({"message": "Password must be at least 8 characters long"}, status=401)
        if len(request.data['password']) > 32:
            return Response({"message": "Password must be at most 32 characters long"}, status=401)
        
        # create user if all checks pass
        super().post(request, *args, **kwargs)

        user = Account.objects.get(username=request.data['username'])
        refresh = RefreshToken.for_user(user)
        OnlineStatus.objects.create(user=user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "username": request.data['username'],
                "email": request.data['email'],
                "profile_image": user.get_profile_image_url()
            }
        }, status=201)


# custom error message for login if credentials are invalid
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        # Validate the username and password
        serializer.is_valid(raise_exception=True)

        user = Account.objects.get(username=request.data['username'])

        if user.enabled_2FA:
            user.set_date_2FA()
            return Response({"id": user.id}, status=200)

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "profile_image": user.get_profile_image_url(user),
            }
        })


# *******************************************************************************************************************
# ************************************************** 2FA Enable *****************************************************
# *******************************************************************************************************************

class Check_two_factor_code(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        if not request.data['id']:
            return Response({"message": "User id is required"}, status=400)
        if not request.data['code']:
            return Response({"message": "2FA code is required"}, status=400)
        user = Account.objects.get(id=request.data['id'])
        if not user.waiting_2FA:
            return Response({"message": "Invalid request"}, status=400)
        if user.compare_date_2FA():
            user.set_date_2FA()
        if user.is_otp_valid(request.data['code']) and user.waiting_2FA is not None:
            refresh = RefreshToken.for_user(user)
            # Reset the waiting_2FA field
            user.waiting_2FA = None
            user.save()
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "profile_image": user.get_profile_image_url()
                }
            }, status=200)
        return Response({"message": "Invalid 2FA code"}, status=400)


# *******************************************************************************************************************
# ********************************************* User Profile & Update ***********************************************
# *******************************************************************************************************************

# will return user info of the logged in user
class ProfileView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "profile_image": user.get_profile_image_url(),
            "display_name": user.display_name,
            "enabled_2FA": user.enabled_2FA,
            "qrcode_2FA": user.qrcode_2FA.url
        })


# return user info by username, eg: /user/rookie/ will return user info of user with username rookie
class UserProfile(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'username'

    def get_object(self):
        try:
            return Account.objects.get(username=self.kwargs['username'])
        except Account.DoesNotExist:
            return None
    
    def get(self, request, *args, **kwargs):
        user = self.get_object()

        if user is None:
            return Response({"message": "User not found"}, status=404)

        return Response({
            "id": user.id,
            "username": user.username,
            "profile_image": user.get_profile_image_url(),
            "display_name": user.display_name,
            "online_status": OnlineStatus.objects.get(user=user).is_online
        })

# update user profile
class UpdateProfileView(generics.UpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = UpdateProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        token = self.request.headers.get('Authorization')
        if token is None or not token.startswith('Bearer '):
            return Response({"message": "Unauthorized"}, status=401)
        token = token[7:]
        try :
            UntypedToken(token)
        except:
            return Response({"message": "Unauthorized"}, status=401)
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        new_password = serializer.validated_data.get('password', None)
        if new_password:
            instance.set_password(new_password)
            instance.save()

        if 'profile_image' in serializer.validated_data:
            serializer.validated_data["profile_image"] = instance.get_profile_image_url()

        return Response(serializer.validated_data)



# *******************************************************************************************************************
# ***************************************************** 42 AUTH *****************************************************
# *******************************************************************************************************************

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URI = os.environ.get('REDIRECT_URI')

class RedirectTo42View(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return f'https://api.intra.42.fr/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code'

class Handle42AuthView(APIView):
    permission_classes = [permissions.AllowAny]

    def find_or_create_intra_user(self, user_info):
        User = get_user_model()
        
        # If the user already exists, return the user
        if User.objects.filter(login_intra=user_info['login']).exists():
            return User.objects.get(login_intra=user_info['login'])
        
        # Create the user if it doesn't exist
        username_base = user_info['login']
        username = username_base
        attempts = 0

        while User.objects.filter(username=username).exists():
            attempts += 1
            username = f'{username_base}{str(attempts)}'

        user = User.objects.create_user(
            username=username,
            email=user_info['email'],
            login_intra=user_info['login'],
            password=user_info['login']
        )
        user.save()
        return user
    
    def post(self, request, *args, **kwargs):
        code = request.data['code']


        if code is None:
            return Response({"message": "Code is required"}, status=400)

        response = requests.post(
            f'https://api.intra.42.fr/oauth/token',
            data={
                'grant_type': 'authorization_code',
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'redirect_uri': REDIRECT_URI,
                'code': code
            }
        )


        if response.status_code != 200:
            return Response({"message": "Authentication failed"}, status=400)

        authorizations = response.json()
        access_token = authorizations['access_token']
        user_response = requests.get(
            'https://api.intra.42.fr/v2/me',
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )

        if user_response.status_code != 200:
            return Response({"message": "Failed to retrieve user info"}, status=400)

        user_info = user_response.json()
        user = self.find_or_create_intra_user(user_info)
        refresh = RefreshToken.for_user(user)

        return JsonResponse({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "profile_image": user.get_profile_image_url()
            }
        })

# *******************************************************************************************************************
# ************************************************** Online Status **************************************************
# *******************************************************************************************************************

class UserOnlineStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, username, *args, **kwargs):
        try:
            user = Account.objects.get(username=username)
            serializer = UserOnlineSerializer(user)
            return Response(serializer.data)
        except Account.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
