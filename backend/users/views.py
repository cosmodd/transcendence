from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Account
from .serializers import AccountSerializer, ProfileSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import sys

class RegisterView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.AllowAny]

# custom error message for login if credentials are invalid
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # print(request.data, file=sys.stderr)
        serializer.is_valid(raise_exception=True)
        # print(serializer.validated_data, file=sys.stderr)
        print("HERE", file=sys.stderr)
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