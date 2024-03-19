# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        #scope is a dictionary containing information about the connection
        self.sender = self.scope['user']
        self.receiver_id = self.scope['url_route']['kwargs']['receiver_id']
        self.receiver = await self.get_receiver()

        if self.sender.is_authenticated and self.receiver:
            self.chat_room = f"chat_{min(self.sender.id, self.receiver.id)}_{max(self.sender.id, self.receiver.id)}"

            # Join chat room created with the id of the sender and receiver.
            #channel_name is a unique identifier for the connection
            await self.channel_layer.group_add(
                self.chat_room,
                self.channel_name
            )

            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        pass