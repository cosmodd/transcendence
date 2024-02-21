from rest_framework import serializers
from .models import Account
import sys

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'email', 'password', 'profile_image']
        extra_kwargs = {
            'password': {'write_only': True}
        }

def check_password(raw_password, password):
    return raw_password == password

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=30, required=True)
    password = serializers.CharField(max_length=30, required=True, write_only=True)

    class Meta:
        model = Account
        fields = ['username', 'password']


    def validate(self, data):
        #try to get user with username if not exists raise validation error
        user = Account.objects.filter(username=data['username']).first()
        if not user:
            raise serializers.ValidationError("Invalid username")
        if not check_password(data['password'], user.password):
            raise serializers.ValidationError("Invalid password")
        print("PASSED", file=sys.stderr)
        return data

            

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'email', 'profile_image']