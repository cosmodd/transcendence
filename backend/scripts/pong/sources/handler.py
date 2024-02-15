#!/usr/bin/env python
#debug
import logging
logger = logging.getLogger('websockets')
logger = logging.getLogger()
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
from class_game import *
from constants import *
#from websockets.frames import CloseCode
#from django.core.management import call_command

ROOM = {}
connected_clients = asyncio.Queue()

async def main():
    asyncio.ensure_future(queue())
    async with websockets.serve(handler, "0.0.0.0", 8888):
        await asyncio.Future()  # run forever

# Create room if enough clients
async def queue():
    global connected_clients
    while True:
        await asyncio.sleep(1)
        if connected_clients.qsize() >= 2:
            asyncio.create_task(new_room(await connected_clients.get(), await connected_clients.get()))

async def handler(websocket):
    global connected_clients
    message = await websocket.recv()
    event = json.loads(message)
    assert event[METHOD] == FROM_CLIENT
    await connected_clients.put(websocket)

    # Wait for room creation
    try:
        async for message in websocket:
            event = json.loads(message)
            if (event[DATA_LOBBY_STATE] == DATA_LOBBY_ROOM_CREATED):
                break 
        game, connected = ROOM[event[DATA_LOBBY_ROOM_ID]]
        await ClientRecvLoop(websocket, game, event[DATA_PLAYER])

    except:
        logger.debug("DEBUG::Client left while searching game")
        tmp_connected_clients = asyncio.Queue()
        while not connected_clients.empty():
            client = await connected_clients.get()
            if client != websocket:
                await tmp_connected_clients.put(client)
        connected_clients = tmp_connected_clients
 
async def new_room(client1, client2):
    room_id = secrets.token_urlsafe(3)
    game = Game()
    await game.CreateModel(room_id)
    ROOM[room_id] = game, [client1, client2]

    event = {
        METHOD: FROM_SERVER,
        OBJECT: OBJECT_LOBBY,
        DATA_LOBBY_STATE: DATA_LOBBY_ROOM_CREATED,
        DATA_PLAYER: PLAYER1,
        DATA_INFO_TYPE: DATA_INFO_TYPE_MESSAGE,
        DATA_INFO_TYPE_MESSAGE: "Room found: " + str(room_id),
        DATA_LOBBY_ROOM_ID: room_id
    }
    await client1.send(json.dumps(event))
    event[DATA_PLAYER] = PLAYER2
    await client2.send(json.dumps(event))

    asyncio.ensure_future(ServerSendLoop(game, [client1, client2]))

if __name__ == "__main__":
    asyncio.run(main())