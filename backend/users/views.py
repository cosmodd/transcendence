from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Account
from .serializers import AccountSerializer, ProfileSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import sys
import re

class RegisterView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
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