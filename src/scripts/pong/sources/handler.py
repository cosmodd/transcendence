#!/usr/bin/env python

#debug
import logging
# logger = logging.getLogger('websockets')
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())

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

JOIN = {}


async def main():
    async with websockets.serve(handler, "0.0.0.0", 8888):
        await asyncio.Future()  # run forever

async def handler(websocket):
    lock = asyncio.Lock()
    message = await websocket.recv()

    event = json.loads(message)
    assert event[METHOD] == FROM_CLIENT

	# if OBJECT in event:
    if event[OBJECT] == OBJECT_JOIN:
        await join(websocket, event[DATA_JOINKEY])
    elif event[OBJECT] == OBJECT_CREATE:
        await create(websocket)

async def create(websocket):
    # Init set of WebSocket connections receiving moves
    connected = {websocket}
    game = Game()
    # Init secret token.
    join_key = secrets.token_urlsafe(12)
    JOIN[join_key] = game, connected

    try:
        event = {
            METHOD: FROM_SERVER,
            OBJECT: OBJECT_INFO,
            DATA_INFO_TYPE: DATA_INFO_TYPE_MESSAGE,
            DATA_INFO_TYPE_MESSAGE: join_key
        }
        await websocket.send(json.dumps(event))
        
        # Game loop
        await ClientRecvLoop(websocket, game, PLAYER1, connected)

    finally:
        del JOIN[join_key]


async def join(websocket, join_key):
    try:
        game, connected = JOIN[join_key]
    except KeyError:
        await sender.Error(websocket, "Game not found.")
        return

    connected.add(websocket);

    for ws in connected:
        response = {
            METHOD: FROM_SERVER,
            OBJECT: OBJECT_INFO, 
            DATA_INFO_TYPE: DATA_INFO_TYPE_MESSAGE,
            DATA_INFO_TYPE_MESSAGE: "Both clients are connected!"
        }
        await ws.send(json.dumps(response))

    #Game loop
    try:
        asyncio.ensure_future(ServerSendLoop(game, connected))
        await ClientRecvLoop(websocket, game, PLAYER2, connected)
    finally:
        connected.remove(websocket)




if __name__ == "__main__":
    asyncio.run(main())