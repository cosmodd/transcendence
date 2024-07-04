from rest_framework import serializers
from .models import Friend, FriendRequest, Block

class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ['id', 'user', 'friend', 'created_at']

class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = serializers.SerializerMethodField()
    to_user = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'created_at']

    def get_from_user(self, obj):
        return obj.from_user.username
    
    def get_to_user(self, obj):
        return obj.to_user.username


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ['id', 'user', 'blocked_user', 'created_at']