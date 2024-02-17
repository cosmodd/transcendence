#!/usr/bin/env python
#debug
import logging
logger = logging.getLogger('websockets')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()
import asyncio
import websockets
import secrets
import json
import sender
from gamelogic import ClientRecvLoop, ServerSendLoop
from class_client import Client
from class_game import *
from constants import *
#from websockets.frames import CloseCode
#from django.core.management import call_command

ROOMS = {}
connected_clients = asyncio.Queue()
# disconnected_clients = asyncio.Queue()

async def main():
    asyncio.ensure_future(Matchmaking())
    async with websockets.serve(handler, "0.0.0.0", 8888):
        await asyncio.Future()  # run forever

# Create room if enough new clients
async def Matchmaking():
    global connected_clients
    while True:
        await asyncio.sleep(1)
        if connected_clients.qsize() >= 2:
            client1 = Client(await connected_clients.get(), secrets.token_urlsafe(2), PLAYER1)
            client2 = Client(await connected_clients.get(), secrets.token_urlsafe(2), PLAYER2)
            asyncio.create_task(new_room(client1, client2))

async def handler(websocket):
    global connected_clients
    message = await websocket.recv()
    event = json.loads(message)
    assert event[METHOD] == FROM_CLIENT

    # Reconnection
    room_id = event[DATA_LOBBY_ROOM_ID]
    uuid = event[DATA_PLAYER_UUID]
    if (len(room_id) != 0):
        if room_id in ROOMS:
            game = ROOMS[room_id]
            for c in game.disconnected:
                if (uuid == c.uuid):
                    logger.debug("FOUND ROOM - READY TO RECONNECT")
                    game.disconnected.remove(c)
                    c.ws = websocket
                    game.connected.append(c)
                    game.match_is_paused = False
                    await ClientRecvLoop(websocket, game, c.name)

    # New client
    await connected_clients.put(websocket)

    # Searching match
    try:
        async for message in websocket:
            event = json.loads(message)
            if (event[DATA_LOBBY_STATE] == DATA_LOBBY_ROOM_CREATED):
                break 
        game = ROOMS[event[DATA_LOBBY_ROOM_ID]]
        await ClientRecvLoop(websocket, game, event[DATA_PLAYER])

	# Client left while searching match
    except:
        # logger.debug("DEBUG::Client left while searching game")
        tmp_connected_clients = asyncio.Queue()
        while not connected_clients.empty():
            client = await connected_clients.get()
            if client != websocket:
                await tmp_connected_clients.put(client)
        connected_clients = tmp_connected_clients
 
async def new_room(client1: Client, client2: Client):
    room_id = secrets.token_urlsafe(3)
    game = Game(room_id, [client1, client2])
    await game.CreateModel()
    ROOMS[room_id] = game

    # TODO -> loop to send
    event = {
        METHOD: FROM_SERVER,
        OBJECT: OBJECT_LOBBY,
        DATA_LOBBY_STATE: DATA_LOBBY_ROOM_CREATED,
        DATA_INFO_TYPE: DATA_INFO_TYPE_MESSAGE,
        DATA_INFO_TYPE_MESSAGE: "Room found: " + str(room_id),
        DATA_LOBBY_ROOM_ID: room_id,
        DATA_PLAYER: game.connected[0].name,
        DATA_PLAYER_UUID: game.connected[0].uuid
    }
    await client1.ws.send(json.dumps(event))
    event[DATA_PLAYER] = game.connected[1].name
    event[DATA_PLAYER_UUID] = game.connected[1].uuid
    await client2.ws.send(json.dumps(event))

    await asyncio.ensure_future(ServerSendLoop(game))
    del ROOMS[game.room_id]

if __name__ == "__main__":
    asyncio.run(main())