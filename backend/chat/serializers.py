from rest_framework import serializers
from .models import Room, RoomMessages

class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class RoomMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomMessages
        fields = '__all__'