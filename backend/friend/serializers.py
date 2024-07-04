from rest_framework import serializers

from users.models import Account
from .models import Friend, FriendRequest, Block

class SimpleAccountSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ['display_name', 'username', 'profile_image', 'is_online']

    def get_profile_image(self, obj):
        return obj.get_profile_image_url()

class FriendSerializer(serializers.ModelSerializer):
    user = SimpleAccountSerializer()
    friend = SimpleAccountSerializer()

    class Meta:
        model = Friend
        fields = ['id', 'user', 'friend', 'created_at']

class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = SimpleAccountSerializer()
    to_user = SimpleAccountSerializer()

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'created_at']

class BlockSerializer(serializers.ModelSerializer):
    user = SimpleAccountSerializer()
    blocked_user = SimpleAccountSerializer()

    class Meta:
        model = Block
        fields = ['id', 'user', 'blocked_user', 'created_at']