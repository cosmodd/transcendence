# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.exceptions import InvalidTokenError, TokenError
from rest_framework_simplejwt.tokens import AccessToken
from .models import Rooms, RoomMessages
import json
import asyncio


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # accept the connection if the user is authenticated
        user = await self.get_user_from_token()
        if user.username == "":
            await self.close()
            return 
        self.user = user
        self.room_group_name = f'chat_{self.user.id}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.channel_layer.group_add(
            "users",
            self.channel_name
        )
        await self.accept()
        await self.channel_layer.group_send(
            "users",
            {
                'type': 'user_status',
                'user': self.user.username,
                'status': 'online'
            }
        )

    async def disconnect(self, close_code):
        #TODO: check if the user has open multiple tabs
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.channel_layer.group_discard(
            "users",
            self.channel_name
        )
        await self.channel_layer.group_send(
            "users",
            {
                'type': 'user_status',
                'user': self.user.username,
                'status': 'offline'
            }
        )

    async def receive(self, text_data):
        data_json = json.loads(text_data)
        message = data_json['message']
        room_name = data_json['room_name']
        room = Rooms.objects.get(name=room_name)
        if self.user not in room.members.all():
            return
        receivers = room.members.all()
        for receiver in receivers:
            await self.channel_layer.group_send(
                f'chat_{receiver.id}',
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': self.user.username,
                    'room_name': room_name
                }
            )
        sender = self.user
        room = Rooms.objects.get(name=room_name)
        message = RoomMessages(room=room, sender=sender, message=message)
        message.save()

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        room_name = event['room_name']
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'room_name': room_name
        }))

    async def get_user_from_token(self):
        # extract the token from the headers
        # dictionaries provided by Django Channels scope are expected to be bytes objects rather than Unicode strings 
        auth_header = self.scope.get('headers', {}).get(b'authorization', b'').decode('utf-8')
        if not auth_header.startswith('Bearer '):
            return AnonymousUser()
        try:
            token = auth_header.split(' ')[1]
            access_token = AccessToken(token)
            return access_token.user
        except (InvalidTokenError, TokenError, IndexError):
            return AnonymousUser()