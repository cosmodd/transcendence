from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Rooms, RoomMessages
from .serializers import  RoomsSerializer, MessageSerializer
from users.models import Account

class RoomView(APIView):
    permission_classes = [IsAuthenticated]
    sererializer_class = RoomsSerializer # useless

    def get(self, request):
        rooms = Rooms.objects.filter(members=request.user)
        data = []
        for room in rooms:
            last_message = room.get_last_message()
            data.append({
                'room': room.name,
                'last_message': last_message.message,
                'last_message_sender': last_message.sender.username,
                'chatting_with': room.get_members().exclude(username=request.user.username).first().username
            })
        return Response(data)

class RoomMessagesView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer # useless

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
        return Response(data)
    
class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        current_user = request.user
        target_user = Account.objects.get(username=username)
        room_name = f'chat_{current_user.id}_{target_user.id}'
        room = Rooms.objects.filter(name=room_name)
        if not room.exists():
            room = Rooms.objects.create(name=room_name)
            room.members.add(current_user, target_user)