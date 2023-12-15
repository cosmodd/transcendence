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

PLAYER1, PLAYER2 = "p1", "p2"
# playersMap = {
#     PLAYER1: Paddle((0, 0)),
#     PLAYER2: Paddle((0, 0)),
# }
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
        await play(websocket, PLAYER1, connected)


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
        response = {
            "type": "message", 
            "message": "both clients are connected"
        }
        await ws.send(json.dumps(response))

    #Game loop - temporary
    try:
        await play(websocket, PLAYER2, connected)
    finally:
        connected.remove(websocket)

# Game loop
async def play(websocket, player, connected):
    # opponent = PLAYER2 if player == PLAYER1 else PLAYER1

    async for message in websocket:
            event = json.loads(message)

            # Receive data and transmit to the other - temporary
            if event["type"] == "send" and event["object"] == "paddle":
                # async with lock:
                    # playersMap[player].position = event["position"]
                transmit = {
                    "type": "get",
                    "object": "paddle",
                    "position": [event["position"][0], event["position"][1]]
                }
                for ws in connected:
                    if ws != websocket:
                        await ws.send(json.dumps(transmit))


            # # Send data
            # if event["type"] == "get" and event["object"] == "paddle":
            #     async with lock:
            #         position = playersMap[opponent].position
            #     response = {
            #         "type": "get",
            #         "object": "paddle",
            #         "position": [position[0], position[1]]
            #     }
            #     await websocket.send(json.dumps(response))
                    
                

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