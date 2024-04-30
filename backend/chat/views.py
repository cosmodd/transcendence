from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Rooms, RoomMessages
from .serializers import  RoomsSerializer, RoomMessagesSerializer
from users.models import Account
import sys

class RoomView(APIView):
    permission_classes = [IsAuthenticated]
    sererializer_class = RoomsSerializer # useless

    def get(self, request):
        print("HERE", file=sys.stderr)
        rooms = Rooms.objects.filter(members=request.user)
        data = []
        for room in rooms:
            last_message = room.get_last_message()
            data.append({
                'room': room.name,
                'last_message': last_message.message if last_message else None,
                'last_message_sender': last_message.sender.username if last_message else None,
                'chatting_with': room.get_members().exclude(username=request.user.username).first().username
            })
        if not data:
            return Response({'info': 'No rooms found'}, status=200)
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
                'timestamp': message.timestamp
            })
        if not data:
            return Response({'info': 'No message in this conversation'}, status=200)
        return Response(data)
    
class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        print("HERE", file=sys.stderr)
        current_user = request.user
        target_user = Account.objects.get(username=username)
        room_name = f'chat_{current_user.id}_{target_user.id}'
        print(room_name, file=sys.stderr)
        room = Rooms.objects.filter(name=room_name)
        if not room.exists():
            room = Rooms.objects.create(name=room_name, conversation_type='private')
            room.members.add(current_user, target_user)
        return Response({'room': room_name}, 200)