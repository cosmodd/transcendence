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
from friend.models import Block


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
        await self.channel_layer.group_add( #add the user to the group of all users
            'online_users',
            self.channel_name
        )
        #print list of channels room group name
        print(self.channel_layer.groups, file=sys.stderr)
        await self.accept()
        await self.increment_user_connection_count()

    async def disconnect(self, close_code):
        #TODO: check if the user has open multiple tabs
        await self.decrement_user_connection_count()
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.channel_layer.group_discard(
            'online_users',
            self.channel_name
        )

    async def receive(self, text_data):
        data_json = json.loads(text_data)
        message = data_json.get('message', '')
        room_name = data_json['room_name']
        message_type = data_json.get('message_type', 'text')

        #check if the user is blocked
        blocked = await self.get_blocked_users(room_name)
        if blocked:
            return

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
        room_name = event.get('room_name', '')
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

    async def user_status(self, event):
        message = event['message']
        message_type = event['message_type']
        user = event['user']
        is_online = event['is_online']

        print(f"User status: {user} is online: {is_online}", file=sys.stderr)

        await self.send(text_data=json.dumps({
            'message': message,
            'message_type': message_type,
            'user': user,
            'is_online': is_online
        }))

    async def send_user_online_status(self, is_online):
        message = f'{self.user.username} is now online' if is_online else f'{self.user.username} is now offline'
        await self.channel_layer.group_send(
            'online_users',
            {
                'type': 'user_status',
                'message': message,
                'message_type': 'online_status',
                'user': self.user.username,
                'is_online': is_online
            }
        )

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
        #create a new room for the game
        player1 = room_members[0]
        player2 = room_members[1]
        await self.create_game_room(player1, player2)

    async def increment_user_connection_count(self):
        self.user = await database_sync_to_async(Account.objects.get)(username=self.user.username)
        self.user.connection_count += 1

        if self.user.connection_count == 1:
            self.user.is_online = True
            await self.send_user_online_status(True)
            print(f"-----------------------------------------------------------------", file=sys.stderr)
            print(f"User '{self.user.username}' is online: {self.user.is_online}", file=sys.stderr)
            print(f"-----------------------------------------------------------------", file=sys.stderr)
        
        await database_sync_to_async(self.user.save)()

    async def decrement_user_connection_count(self):
        self.user = await database_sync_to_async(Account.objects.get)(username=self.user.username)
        print(f"User '{self.user.username}' connection count: {self.user.connection_count}", file=sys.stderr)
        self.user.connection_count -= 1

        if self.user.connection_count <= 0:
            self.user.is_online = False
            self.user.connection_count = 0
            await self.send_user_online_status(False)
            print(f"User '{self.user.username}' is online: {self.user.is_online}", file=sys.stderr)
        
        await database_sync_to_async(self.user.save)()

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
            
    async def create_game_room(self, player1, player2):
        import websockets
        import json
        import ssl

        METHOD = "Method"
        DATA_PLAYER_PLAYER1 = "p1"
        DATA_PLAYER_PLAYER2 = "p2"
        print(f"Player1: {player1}", file=sys.stderr)
        print(f"Player2: {player2}", file=sys.stderr)

        uri = "wss://localhost:8888"
        ssl_context = ssl._create_unverified_context()
        async with websockets.connect(uri, ssl=ssl_context) as websocket:
            message = json.dumps({
                METHOD: "from_backend",
                DATA_PLAYER_PLAYER1: player1.username,
                DATA_PLAYER_PLAYER2: player2.username,
            })
            await websocket.send(message) 

    @database_sync_to_async
    def get_user_from_username(self, username):
        return Account.objects.get(username=username)
    
    @database_sync_to_async
    def get_blocked_users(self, room_name):
        room = Rooms.objects.get(name=room_name)
        room_members = list(room.members.all())
        for member in room_members:
            if Block.objects.filter(user=self.user, blocked_user=member).exists():
                return True
        return False
    
    #a function that will be used outside the django project to send a notification to 2 users
async def send_notification(receiver1, receiver2):
    from channels.layers import get_channel_layer
    channel_layer = get_channel_layer()

    receiver1 = await get_user_from_username(receiver1)
    receiver2 = await get_user_from_username(receiver2)
    await channel_layer.group_send(
        f'chat_{receiver1.id}',
        {
            'type': 'chat_message',
            'message': 'You are expected for your next tournament match',
            'sender': 'system',
            'message_type': 'notification'
        }
    )
    await channel_layer.group_send(
        f'chat_{receiver2.id}',
        {
            'type': 'chat_message',
            'message': 'You are expected for your next tournament match',
            'sender': 'system',
            'message_type': 'notification'
        }
    )

@database_sync_to_async
def get_user_from_username(username):
    return Account.objects.get(username=username)
