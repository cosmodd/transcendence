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
from datetime import datetime
import sender
from gamelogic import ClientLoop, ServerLoop
from class_client import Client
from class_game import *
from constants import *
#from websockets.frames import CloseCode
#from django.core.management import call_command

ROOMS = {}
room_lock = asyncio.Lock()
connected_clients = asyncio.Queue()
# disconnected_clients = asyncio.Queue()

async def main():
    asyncio.ensure_future(Matchmaking())
    async with websockets.serve(Handler, "0.0.0.0", 8888):
        await asyncio.Future()  # run forever

# Create room if enough new clients
async def Matchmaking():
    global connected_clients
    while True:
        await asyncio.sleep(1)
        if connected_clients.qsize() >= 2:
            client1 = Client(await connected_clients.get(), secrets.token_urlsafe(2), PLAYER1)
            client2 = Client(await connected_clients.get(), secrets.token_urlsafe(2), PLAYER2)
            asyncio.create_task(NewRoom([client1, client2]))

async def Handler(websocket):
    global connected_clients
    message = await websocket.recv()
    event = json.loads(message)
    assert event[METHOD] == FROM_CLIENT

    # Expected for a tournament ?
    # Expected for a duel ?

    try:
        # Reconnection ?
        await Reconnection(websocket, event)

        # New client
        await connected_clients.put(websocket)

        # Searching match
        async for message in websocket:
            event = json.loads(message)
            if (event[DATA_LOBBY_STATE] == DATA_LOBBY_ROOM_CREATED):
                break 
        async with room_lock: game = ROOMS[event[DATA_LOBBY_ROOM_ID]]
        await ClientLoop(websocket, game, event[DATA_PLAYER])

	# Client left while searching for a match
    except Exception as e:
        await RemoveClientFromQueue(websocket)

async def Reconnection(websocket, event):
    room_id = event.get(DATA_LOBBY_ROOM_ID, "")
    uuid = event.get(DATA_PLAYER_UUID, "")
    async with room_lock:
        if room_id and room_id in ROOMS:
            game = ROOMS[room_id]
            async with game.reconnection_lock:
                for c in game.disconnected:
                    if (uuid == c.uuid):
                        # logger.debug("FOUND ROOM - READY TO RECONNECT")
                        game.disconnected.remove(c)
                        c.ws = websocket
                        game.connected.append(c)
                        await sender.ToAll(game.MessageBuilder.OpponentReconnected(), game.connected)
                        await c.ws.send(game.MessageBuilder.Reconnection())
                        game.match_is_paused = False
                        game.pause_time_added += (datetime.now() - game.pause_timer).total_seconds()
                        game.reconnection_lock.release()
                        await ClientLoop(websocket, game, c.name)
 
async def NewRoom(clients):
    room_id = secrets.token_urlsafe(3)
    game = Game(room_id, clients)
    await game.CreateModel()
    async with room_lock: ROOMS[room_id] = game

    for i in range(len(clients)):
        await clients[i].ws.send(game.MessageBuilder.NewRoomInfoFor(i))

    await ServerLoop(game)
    async with room_lock: del ROOMS[game.room_id]

async def RemoveClientFromQueue(websocket):
    global connected_clients
    # logger.debug("DEBUG::Client left while searching game")
    tmp_connected_clients = asyncio.Queue()
    while not connected_clients.empty():
        client = await connected_clients.get()
        if client != websocket:
            await tmp_connected_clients.put(client)
    connected_clients = tmp_connected_clients


if __name__ == "__main__":
    asyncio.run(main())