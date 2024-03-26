# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.exceptions import InvalidTokenError, TokenError
from rest_framework_simplejwt.tokens import AccessToken
from .models import RoomName, RoomMessages
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # accept the connection if the user is authenticated
        user = await self.get_user_from_token()
        if user.username == "":
            await self.close()
        else:
            await self.accept()


    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        pass

    async def chat_message(self, event):
        pass

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