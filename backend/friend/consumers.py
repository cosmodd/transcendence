# chat/consumers.py
from datetime import timedelta, datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from .models import Rooms, RoomMessages
from asgiref.sync import sync_to_async
import json, sys
from channels.db import database_sync_to_async
from users.models import Account
import asyncio
from time import sleep


class StatusOnline(AsyncWebsocketConsumer):
    async def connect(self):
        token = self.scope.get('url_route', {}).get('kwargs', {}).get('token')
        user = await self.get_user_from_token(token)
        if user.is_anonymous:
            await self.close()
        else:
            self.user = user
            await self.channel_layer.group_add(
                f'user_{self.user.id}',
                self.channel_name
            )
            await self.set_user_status(self.user, True)
            await self.accept()

    async def disconnect(self, close_code):
        await self.set_user_status(self.user, False)
        await self.channel_layer.group_discard(
            f'user_{self.user.id}',
            self.channel_name
        )

    async def receive(self, text_data):
        pass

    async def set_user_status(self, user, is_online):
        await sync_to_async(Account.objects.filter(pk=user.id).update)(
            is_online=is_online
        )
        await self.channel_layer.group_send(
            'online_status',
            {
                'type': 'user_status',
                'user_id': user.id,
                'is_online': is_online
            }
        )

    async def user_status(self, event):
        await self.send(text_data=json.dumps({
            'user_id': event['user_id'],
            'is_online': event['is_online']
        }))

    async def get_user_from_token(self, token):
        try:
            jwt_authentication = JWTAuthentication()
            access_token = AccessToken(token)
            print('access_token stage', file=sys.stderr)
            user = await sync_to_async(jwt_authentication.get_user)(access_token)
            # return the user if authenticated, otherwise return AnonymousUser
            # user is a tuple of (user, token)
            if user is not None:
                return user
            else:
                return AnonymousUser()
        except:
            return AnonymousUser()
        