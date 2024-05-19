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
import asyncio


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # accept the connection if the user is authenticated
        token = self.scope.get('url_route', {}).get('kwargs', {}).get('token')
        user = await self.get_user_from_token(token)
        print(f'Websocket request from User: {user}', file=sys.stderr)
        if user.username == "":
            await self.close()
            return 
        self.user = user
        self.room_group_name = f'chat_{self.user.id}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        #print list of channels room group name
        print(self.channel_layer.groups, file=sys.stderr)
        await self.accept()


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

    async def receive(self, text_data):
        data_json = json.loads(text_data)
        message = data_json.get('message', '')
        room_name = data_json['room_name']
        message_type = data_json.get('message_type', 'text')

        print(f"Message_type: {message_type}", file=sys.stderr)

        if message_type == 'invitation':
            await self.send_invitation(room_name)
        elif message_type == 'accepted':
            await self.handle_game_invitation(message, room_name)
        else:
            await self.send_message(message, room_name)
        

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        room_name = event['room_name']
        message_type = event.get('message_type', 'text')
        timestamp = event.get('timestamp', None)
        is_accepted = event.get('is_accepted', False)

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'room_name': room_name,
            'message_type': message_type,
            'timestamp': timestamp,
            'is_accepted': is_accepted
        }))

    async def send_message(self, message, room_name):
        room = await self.get_chat_room(room_name)
        room_members = await self.get_chat_room_members(room)

        if self.user not in room_members:
            return
        print (f"User test: {self.user}", file=sys.stderr)
        for receiver in room_members:
            print("test", file=sys.stderr)
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
        print(f"Sender: {sender}", file=sys.stderr)
        await self.save_message(sender, message, room)

    async def send_invitation(self, room_name):
        room = await self.get_chat_room(room_name)
        room_members = await self.get_chat_room_members(room)

        if self.user not in room_members:
            return
        print (f"User test INVITATION: {self.user}", file=sys.stderr)
        messages = await self.get_all_messages(room)
        print(f"Messages INVITATION: {messages}", file=sys.stderr)
        for message in messages:
            if message.message_type == 'invitation' and message.status == 'pending':
                string_format = "%Y-%m-%d %H:%M:%S"
                current_time = datetime.now()
                message_time = message.timestamp
                invit_date = datetime.strptime(message_time.strftime(string_format), string_format)
                invit_date = invit_date + timedelta(minutes=120)
                diff = current_time - invit_date
                print(f"\033[91mCurrent time: {current_time}\033[00m", file=sys.stderr)
                print(f"\033[91mInvitation time: {invit_date}\033[00m", file=sys.stderr)
                print(f"\033[91mTime difference: {diff}\033[00m", file=sys.stderr)
                if diff.total_seconds() > 60:
                    await self.update_invitation_status(room, 'expired')
                elif message.status == 'pending':
                    return
        
        for receiver in room_members:
            await self.channel_layer.group_send(
                f'chat_{receiver.id}',
                {
                    'type': 'chat_message',
                    'message': f'{self.user.username} has invited you to join a pong party',
                    'sender': self.user.username,
                    'room_name': room_name,
                    'message_type': 'invitation',
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'is_accepted': False
                }
            )
        sender = self.user
        await self.save_message(
            sender, 
            f'{self.user.username} has invited you to join a pong party', 
            room, message_type='invitation',
            status='pending')
        
    async def handle_game_invitation(self, message, room_name):
        room = await self.get_chat_room(room_name)
        room_members = await self.get_chat_room_members(room)

        if self.user not in room_members:
            return
        messages = await self.get_all_messages(room)
        for message in messages:
            if message.message_type == 'invitation' and message.status == 'pending':
                string_format = "%Y-%m-%d %H:%M:%S"
                current_time = datetime.now()
                message_time = message.timestamp
                invit_date = datetime.strptime(message_time.strftime(string_format), string_format)
                invit_date = invit_date + timedelta(minutes=120)
                diff = current_time - invit_date
                print(f"\033[91mCurrent time: {current_time}\033[00m", file=sys.stderr)
                print(f"\033[91mInvitation time: {invit_date}\033[00m", file=sys.stderr)
                print(f"\033[91mTime difference: {diff}\033[00m", file=sys.stderr)
                if diff.total_seconds() > 60:
                    await self.update_invitation_status(room, 'expired')
                    return
                elif message.status == 'pending':
                    print(f"Invitation status normaly pending: {message.status}", file=sys.stderr)
                    await self.update_invitation_status(room, 'accepted')
                    print("Invitation after accepted", file=sys.stderr)

        for receiver in room_members:
            await self.channel_layer.group_send(
                f'chat_{receiver.id}',
                {
                    'type': 'chat_message',
                    'message': 'Invitation accepted',
                    'sender': self.user.username,
                    'room_name': room_name,
                    'message_type': 'notification',
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'is_accepted': True
                }
            )

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
        
    @database_sync_to_async
    def get_chat_room(self, room_name):
        return Rooms.objects.get(name=room_name)

    @database_sync_to_async
    def get_chat_room_members(self, room):
        return list(room.members.all())

    @database_sync_to_async
    def save_message(self, sender, message, room, message_type='text', status=None):
        message = RoomMessages(sender=sender, message=message, room=room, message_type=message_type, status=status)
        message.save()

    @database_sync_to_async
    def get_all_messages(self, room):
        return list(RoomMessages.objects.filter(room=room))
    
    @database_sync_to_async
    def update_invitation_status(self, room, status):
        messages = list(RoomMessages.objects.filter(room=room))
        for message in messages:
            if message.message_type == 'invitation' and message.status == 'pending':
                message.status = status
                message.save()
                return