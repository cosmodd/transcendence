from rest_framework import serializers
from .models import Rooms, RoomMessages

class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = '__all__'

class RoomMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomMessages
        fields = '__all__'