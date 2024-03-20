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

TOKEN_TO_GAME = {}
TOKEN_TO_CURRENTLY_QUEUING = {}
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
            # todo : une ligne
            client1 = await connected_clients.get()
            client1.name = PLAYER1
            client2 = await connected_clients.get()
            client2.name = PLAYER2
            asyncio.create_task(NewRoom([client1, client2]))

async def Handler(websocket):
    global connected_clients
    message = await websocket.recv()
    event = json.loads(message)
    assert event[METHOD] == FROM_CLIENT
    client = Client(websocket, event[DATA_PLAYER_TOKEN])

    # Expected for a tournament ?
    # Expected for a duel ?

    try:
        # Reconnection (or connection, for duel/tournament)
        await Reconnection(client, event)

        # Client wanting to queue
        if client.token in TOKEN_TO_CURRENTLY_QUEUING:
            await client.ws.send(json.dumps({METHOD: FROM_SERVER, OBJECT: OBJECT_INFO, DATA_INFO_TYPE: DATA_INFO_TYPE_ERROR, DATA_INFO_TYPE_ERROR: "Already present in a lobby."}));
            raise Exception("Client already present in a lobby.")
        await connected_clients.put(client)
        TOKEN_TO_CURRENTLY_QUEUING[client.token] = True

        # Searching match
        async for message in websocket:
            event = json.loads(message)
            if (event[DATA_LOBBY_STATE] == DATA_LOBBY_ROOM_CREATED):
                break 
        async with room_lock: game = TOKEN_TO_GAME[client.token]
        try:
            del TOKEN_TO_CURRENTLY_QUEUING[client.token]
        except KeyError as e:
            print(f"KeyError: {e}")
        await ClientLoop(client, game, event[DATA_PLAYER])

	# Client left 
    except Exception as e:
        await RemoveClientFromQueue(client)

async def Reconnection(reconnecting_client, event):
    async with room_lock:
        if reconnecting_client.token and reconnecting_client.token in TOKEN_TO_GAME:
            game = TOKEN_TO_GAME[reconnecting_client.token]
            async with game.reconnection_lock:
                if len(game.disconnected):
                    for c in game.disconnected:
                        if (reconnecting_client.token == c.token):
                            logger.debug("post token == token")
                            logger.debug("FOUND ROOM - READY TO RECONNECT")
                            game.disconnected.remove(c)
                            c.ws = reconnecting_client.ws 
                            game.connected.append(c)
                            await sender.ToAll(game.MessageBuilder.OpponentReconnected(), game.connected)
                            await c.ws.send(game.MessageBuilder.Reconnection())
                            game.match_is_paused = False
                            game.pause_time_added += (datetime.now() - game.pause_timer).total_seconds()
                            game.reconnection_lock.release()
                            room_lock.release()
                            await ClientLoop(c, game, c.name)
                else:
                    room_lock.release()
                    game.reconnection_lock.release()
                    await reconnecting_client.ws.send(json.dumps({METHOD: FROM_SERVER, OBJECT: OBJECT_INFO, DATA_INFO_TYPE: DATA_INFO_TYPE_ERROR, DATA_INFO_TYPE_ERROR: "Already present in a lobby."}));
                    raise Exception("Client already present in a lobby.")
            room_lock.release()
            game.reconnection_lock.release()
 
async def NewRoom(clients):
    room_id = secrets.token_urlsafe(3)
    game = Game(room_id, clients)
    await game.CreateModel()
    clients_tokens = [clients[0].token, clients[1].token]

    for i in range(len(clients)):
        async with room_lock: TOKEN_TO_GAME[clients[i].token] = game
        logger.debug("DEBUG:: added a client to TOKEN_TO_GAME")
        await clients[i].ws.send(game.MessageBuilder.NewRoomInfoFor(i))

    await ServerLoop(game)
    for i in range(len(clients_tokens)):
        async with room_lock: del TOKEN_TO_GAME[clients_tokens[i]]
        logger.debug("DEBUG:: removed a client from TOKEN_TO_GAME")

async def RemoveClientFromQueue(client):
    try:
        del TOKEN_TO_CURRENTLY_QUEUING[client.token]
    except KeyError as e:
        print(f"KeyError: {e}")
    global connected_clients
    # logger.debug("DEBUG::Client left while searching game")
    tmp_connected_clients = asyncio.Queue()
    while not connected_clients.empty():
        curr_client = await connected_clients.get()
        if curr_client.ws != client.ws:
            await tmp_connected_clients.put(curr_client)
    connected_clients = tmp_connected_clients


if __name__ == "__main__":
    asyncio.run(main())