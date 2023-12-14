#!/usr/bin/env python

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

    # Init secret token.
    join_key = secrets.token_urlsafe(12)
    JOIN[join_key] = connected

    try:
        event = {
            "type": "init",
            "join": join_key,
        }
        await websocket.send(json.dumps(event))
        
        # Game loop - temporary
        async for message in websocket:
            print(message)


    finally:
        del JOIN[join_key]

async def join(websocket, join_key):
    try:
        connected = JOIN[join_key]
    except KeyError:
        await error(websocket, "Game not found.")
        return

    connected.add(websocket);

    for ws in connected:
        await ws.send("Both clients are connected !")

    #Game loop - temporary
    async for message in websocket:
        print(message)


async def handler(websocket):
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