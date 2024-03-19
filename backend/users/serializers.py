from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Account
import sys

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'email', 'password', 'profile_image', 'enabled_2FA']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def create(self, validated_data):
        user = Account.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=32, required=True)
    password = serializers.CharField(max_length=32, required=True, write_only=True)

    class Meta:
        model = Account
        fields = ['username', 'password']


    def validate(self, data):
        #try to get user with username if not exists raise validation error
        user = Account.objects.filter(username=data['username']).first()
        if not user:
            raise serializers.ValidationError({"username": "No users with that username"})
        if not user.check_password(data['password']):
            raise serializers.ValidationError({"password": "Incorrect password"})
        # print("PASSED", file=sys.stderr)
        return data



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'email', 'profile_image', 'display_name', 'enabled_2FA', 'qrcode_2FA']

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['display_name', 'profile_image', 'email', 'password', 'enabled_2FA', 'username']