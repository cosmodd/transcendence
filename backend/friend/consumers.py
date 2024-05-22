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


class StatusOnline(AsyncWebsocketConsumer):
    async def connect(self):
        # accept the connection if the user is authenticated
        token = self.scope.get('url_route', {}).get('kwargs', {}).get('token')
        user = await self.get_user_from_token(token)
        if user.username == "":
            await self.close()
            return 
        await self.close_old_connection(user)
        #add all user in same group to know if they are online or not
        self.room_group_name = 'online_status'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        pass

    async def status_online(self, event):
        pass

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