from django.views.generic import RedirectView, View
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, parsers
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import UntypedToken
from .models import Account
from .serializers import AccountSerializer, ProfileSerializer, LoginSerializer, UpdateProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import re, requests, random, string, os, sys
from django.http import JsonResponse
from datetime import datetime

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

        # length of username should be between 2 and 30 characters
        if len(request.data['username']) < 2 or len(request.data['username']) > 30:
            return Response({"message": "Username must be between 2 and 30 characters long"}, status=401)
        # username should contain only letters, numbers, underscores and dots
        if not re.match("^[a-zA-Z0-9_.]*$", request.data['username']):
            return Response({"message": "Username can only contain letters, numbers, underscores and dots"}, status=401)
        # not allow consecutive dots or underscores
        if ".." in request.data['username'] or "__" in request.data['username']:
            return Response({"message": "Username can't have consecutive dots or underscores"}, status=401)
        # email should be valid format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", request.data['email']):
            return Response({"message": "Invalid email"}, status=401)
        # create user if all checks pass
        return super().post(request, *args, **kwargs)
        

# custom error message for login if credentials are invalid
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid() and "username" in serializer.errors:
            return Response({"message": "Invalid username"}, status=401)
        if not serializer.is_valid() and "password" in serializer.errors:
            return Response({"message": "Invalid password"}, status=401)
        # print(serializer.validated_data, file=sys.stderr)
        user = Account.objects.get(username=request.data['username'])
        if user.enabled_2FA:
            user.set_date_2FA()
            return Response({"id": user.id}, status=200)
        refresh = RefreshToken.for_user(user)
        return Response(
        {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "profile_image": user.profile_image.url if user.profile_image else None
            }
        }
        )


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
            return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "profile_image": user.profile_image.url
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

# return user info by username, eg: /user/rookie/ will return user info of user with username rookie
class UserProfile(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'username'

    def get_object(self):
        return Account.objects.get(username=self.kwargs['username'])
    
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

    

# *******************************************************************************************************************
# ***************************************************** 42 AUTH *****************************************************
# *******************************************************************************************************************

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URI = os.environ.get('REDIRECT_URI')

# Auth with 42
class AuthentificationWith42View(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return f'https://api.intra.42.fr/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code'

class Handle42CallbackView(View):

    def manage_intra_user(self, user_info):
        User = get_user_model()
        #if login_42 already exists, return the user
        if User.objects.filter(login_intra=user_info['login']).exists():
            user = User.objects.get(login_intra=user_info['login'])
            refresh = RefreshToken.for_user(user)
            return JsonResponse(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "profile_image": user.profile_image.url if user.profile_image else None
                    }
                }, status=302, headers={'Location': 'http://localhost:8080/'}
            )

        username_base = user_info['login']
        attempts = 0
        #randomize a number in int 
        nb = random.randint(0, 9999)
        while User.objects.filter(username=username_base).exists():
            #convert int to string
            nb += attempts
            username_base = f'{user_info["login"]}{str(nb)}'
            attempts += 1
        user = User.objects.create_user(
            email=user_info['email'],
            username=username_base,
            login_intra=user_info['login'],
            password='42password'
        )
        refresh = RefreshToken.for_user(user)
        # return user info and tokens and redirect to frontend home page
        return JsonResponse(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "profile_image": user.profile_image.url if user.profile_image else None
                }
            }, status=302, headers={'Location': 'http://localhost:8080/'}
        )

    def get(self, request, *args, **kwargs):
        print("HERE 2", file=sys.stderr)
        #authorization code : None means user denied the request for authorization
        code = request.GET.get('code')

        print("HERE", file=sys.stderr)
        if code:
            response = requests.post('https://api.intra.42.fr/oauth/token', data={
                'grant_type': 'authorization_code',
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'code': code,
                'redirect_uri': REDIRECT_URI,
            })
            
            if response.status_code == 200:
                # extract the access token from the response
                access_token = response.json().get('access_token')
                # get user info from 42 api
                user_info_response = requests.get('https://api.intra.42.fr/v2/me', headers={
                    'Authorization': f'Bearer {access_token}',
                })

                if user_info_response.status_code == 200:
                    user_info = user_info_response.json()
                    #print user_info to see what you can use in stdin
                    print(user_info, file=sys.stderr)
                    return self.manage_intra_user(user_info)

        return JsonResponse({'error': 'Authentication failed'}, status=400)

