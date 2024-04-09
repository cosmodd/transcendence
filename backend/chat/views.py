from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Rooms, RoomMessages
from .serializers import  RoomsSerializer, MessageSerializer

class RoomView(APIView):
    permission_classes = [IsAuthenticated]

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