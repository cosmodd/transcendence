#!/usr/bin/env python

#debug
import logging
logger = logging.getLogger('websockets')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

import asyncio
import django
import websockets
import os
import secrets
import json

import sender
from gamelogic import ClientRecvLoop, ServerSendLoop
from class_game import *
from constants import *
#from sesame.utils import get_user
#from websockets.frames import CloseCode

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

#from django.core.management import call_command

ROOM = {}
connected_clients = asyncio.Queue()

async def main():
    asyncio.ensure_future(queue())

    async with websockets.serve(handler, "0.0.0.0", 8888):
        await asyncio.Future()  # run forever

# Create room if enough clients
async def queue():
    while True:
        await asyncio.sleep(1)
        if connected_clients.qsize() >= 2:
            asyncio.create_task(new_room())

async def handler(websocket):
    message = await websocket.recv()
    event = json.loads(message)
    assert event[METHOD] == FROM_CLIENT
    await connected_clients.put(websocket)

    # TODO try disconnection
    event = {}
    async for message in websocket:
        event = json.loads(message)
        if (event[DATA_LOBBY_STATE] == DATA_LOBBY_ROOM_CREATED):
            break 
    
    game, connected = ROOM[event["Room_ID"]]
    await ClientRecvLoop(websocket, game, event[DATA_PLAYER], connected, event["Room_ID"])
    
    
async def new_room():
    client1 = await connected_clients.get()
    client2 = await connected_clients.get()

    game = Game()
    room_id = secrets.token_urlsafe(3)
    ROOM[room_id] = game, [client1, client2]

    event = {
        METHOD: FROM_SERVER,
        OBJECT: OBJECT_LOBBY,
        DATA_LOBBY_STATE: DATA_LOBBY_ROOM_CREATED,
        DATA_PLAYER: PLAYER1,
        DATA_INFO_TYPE: DATA_INFO_TYPE_MESSAGE,
        DATA_INFO_TYPE_MESSAGE: "Room created",
        "Room_ID": room_id
    }
    await client1.send(json.dumps(event))
    event = {
        METHOD: FROM_SERVER,
        OBJECT: OBJECT_LOBBY,
        DATA_LOBBY_STATE: DATA_LOBBY_ROOM_CREATED,
        DATA_PLAYER: PLAYER2,
        DATA_INFO_TYPE: DATA_INFO_TYPE_MESSAGE,
        DATA_INFO_TYPE_MESSAGE: "Room created",
        "Room_ID": room_id
    }
    await client2.send(json.dumps(event))

    
# async def create(websocket):
#     # Init set of WebSocket connections receiving moves
#     connected = {websocket}
#     game = Game()
#     # Init secret token.
#     join_key = secrets.token_urlsafe(3)
#     JOIN[join_key] = game, connected

#     try:
#         event = {
#             METHOD: FROM_SERVER,
#             OBJECT: OBJECT_INFO,
#             DATA_INFO_TYPE: DATA_INFO_TYPE_MESSAGE,
#             DATA_INFO_TYPE_MESSAGE: join_key
#         }
#         await websocket.send(json.dumps(event))
        
#         # Game loop
#         await ClientRecvLoop(websocket, game, PLAYER1, connected)

#     finally:
#         del JOIN[join_key]


# async def join(websocket, join_key):
#     try:
#         game, connected = JOIN[join_key]
#     except KeyError:
#         await sender.Error(websocket, "Game not found.")
#         return

#     connected.add(websocket);

#     for ws in connected:
#         response = {
#             METHOD: FROM_SERVER,
#             OBJECT: OBJECT_INFO, 
#             DATA_INFO_TYPE: DATA_INFO_TYPE_MESSAGE,
#             DATA_INFO_TYPE_MESSAGE: "Both clients are connected!"
#         }
#         await ws.send(json.dumps(response))

#     #Game loop
#     try:
#         asyncio.ensure_future(ServerSendLoop(game, connected))
#         await ClientRecvLoop(websocket, game, PLAYER2, connected)
#     finally:
#         connected.remove(websocket)




if __name__ == "__main__":
    asyncio.run(main())