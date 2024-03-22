# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.exceptions import InvalidTokenError, TokenError
from rest_framework_simplejwt.tokens import AccessToken
from .models import Message, UserConversation, Conversation, WebsocketToken
from uuid import uuid4
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # accept the connection if the user is authenticated
        user = await self.get_user_from_token()
        if user.username == "":
            await self.close()
        else:
            WebsocketToken.objects.create(user=user, token=uuid4())
            await self.accept()

        await self.channel_layer.group_add(f'user_{user.id}', self.channel_name)

    async def disconnect(self, close_code):
        pass
        

    async def receive(self, text_data):
        sender = await self.get_user_from_token()
        try :
            receiver = text_data.get('receiver')
            # check if the channel_layer group is not discarded
            if f'user_{receiver.id}' in self.channel_layer.groups:
                await self.channel_layer.group_send(
                    f'user_{receiver.id}',
                    {
                        'type': 'chat_message',
                        'message': text_data,
                        'sender': sender.username,
                    }
                )
        except AttributeError:
            pass

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

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