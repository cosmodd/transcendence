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

from objects import Ball, Paddle
from play import play
from pong import *
#from sesame.utils import get_user
#from websockets.frames import CloseCode

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

#from django.core.management import call_command

JOIN = {}

async def error(websocket, message):
    event = {
        "type": "error",
        "message": message,
    }
    await websocket.send(json.dumps(event))


async def create(websocket):
    # Init set of WebSocket connections receiving moves
    connected = {websocket}
    game = Pong()
    # Init secret token.
    join_key = secrets.token_urlsafe(12)
    JOIN[join_key] = game, connected

    try:
        event = {
            "type": "init",
            "join": join_key,
        }
        await websocket.send(json.dumps(event))
        
        # Game loop
        await play(websocket, game, PLAYER1, connected)

    finally:
        del JOIN[join_key]


async def join(websocket, join_key):
    try:
        game, connected = JOIN[join_key]
    except KeyError:
        await error(websocket, "Game not found.")
        return

    connected.add(websocket);

    for ws in connected:
        response = {
            "type": "message", 
            "message": "both clients are connected"
        }
        await ws.send(json.dumps(response))

    #Game loop
    try:
        await play(websocket, game, PLAYER2, connected)
    finally:
        connected.remove(websocket)


async def handler(websocket):
    lock = asyncio.Lock()
    message = await websocket.recv()

    event = json.loads(message)
    assert event["type"] == "init"

    if "join" in event:
        await join(websocket, event["join"])
    else:
        await create(websocket)


async def main():
    async with websockets.serve(handler, "0.0.0.0", 8888):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())