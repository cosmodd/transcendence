import sys
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .consumers import send_notification
from .models import Rooms, RoomMessages
from .serializers import RoomMessagesSerializer
from users.models import Account
from asgiref.sync import async_to_sync

class RoomView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rooms = Rooms.objects.filter(members=request.user)
        data = []
        for room in rooms:
            last_message = room.get_last_message()

            chatting_with = room.members.exclude(username=request.user.username).first()
            if room.members.count() == 1:
                chatting_with = request.user

            data.append({
                'room_name': room.name,
                'last_message': last_message.message if last_message else None,
                'last_message_sender': last_message.sender.username if last_message else None,
                'chatting_with': {
                    'display_name': chatting_with.display_name,
                    'username': chatting_with.username,
                    'is_online': chatting_with.is_online,
                    'profile_image': chatting_with.get_profile_image_url()
                }
            })

        return Response(data)

class RoomMessagesView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomMessagesSerializer # useless

    def get(self, request, room):
        if not Rooms.objects.filter(name=room, members=request.user).exists():
            return Response({'error': 'You are not a member of this room'}, status=400)
        room = Rooms.objects.get(name=room)
        messages = RoomMessages.objects.filter(room=room)
        data = []
        for message in messages:
            data.append({
                'sender': message.sender.username,
                'message': message.message,
                'timestamp': message.timestamp,
                'room_name': room.name,
                'message_type': message.message_type,
                'is_accepted': True if message.status == 'accepted' else False
            })
        return Response(data)
    
class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        current_user = request.user
        target_user = Account.objects.get(username=username)

        if not target_user:
            return Response({'error': 'User not found'}, status=404)

        room_name = f'chat_{current_user.id}_{target_user.id}'
        room = Rooms.objects.filter(name=room_name)

        if not room.exists():
            room = Rooms.objects.create(name=room_name, conversation_type='private')
            room.members.add(current_user, target_user)
        return Response({'room': room_name}, 200)
    
class InternalNotificationView(APIView):
    def post(self, request):
        if request.META.get('REMOTE_ADDR') != '127.0.0.1':
            return Response({'error': 'Unauthorized'}, status=401)
        first_user = request.data.get('user1')
        second_user = request.data.get('user2')
        async_to_sync(send_notification)(first_user, second_user)
        return Response({'info': 'Notification sent'}, status=200)