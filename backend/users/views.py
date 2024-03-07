from django.views.generic import RedirectView, View
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Account
from .serializers import AccountSerializer, ProfileSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import re, requests, random, string, os, sys
from django.http import JsonResponse

class RegisterView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        # check if required fields are present
        if not request.data['username']:
            return Response({"message": "Username is required"}, status=400)
        if not request.data['email']:
            return Response({"message": "Email is required"}, status=400)
        if not request.data['password']:
            return Response({"message": "Password is required"}, status=400)
        
        # length of username should be between 2 and 30 characters
        if len(request.data['username']) < 2 or len(request.data['username']) > 30:
            return Response({"message": "Username must be between 2 and 30 characters long"}, status=400)
        # username should contain only letters, numbers, underscores and dots
        if not re.match("^[a-zA-Z0-9_.]*$", request.data['username']):
            return Response({"message": "Username can only contain letters, numbers, underscores and dots"}, status=400)
        # not allow consecutive dots or underscores
        if ".." in request.data['username'] or "__" in request.data['username']:
            return Response({"message": "Username can't have consecutive dots or underscores"}, status=400)
        # email should be valid format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", request.data['email']):
            return Response({"message": "Invalid email"}, status=400)
        # create user if all checks pass
        return super().post(request, *args, **kwargs)
        

# custom error message for login if credentials are invalid
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid() and "non_field_errors" in serializer.errors:
            return Response({"message": "Invalid username"}, status=400)
        if not serializer.is_valid() and "password" in serializer.errors:
            return Response({"message": "Invalid password"}, status=400)
        # print(serializer.validated_data, file=sys.stderr)
        user = Account.objects.get(username=request.data['username'])
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


class ProfileView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URI = os.environ.get('REDIRECT_URI')

# Auth with 42
class AuthentificationWith42View(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        print("HERE 1", file=sys.stderr)
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
                }
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
            }, status=201
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

        return Response({'error': 'Authentication failed'}, status=400)

