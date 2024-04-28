#!/usr/bin/env python
#debug
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
import traceback
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()
import asyncio
import websockets
import json
from datetime import datetime
import sender
from gamelogic import ClientLoop, ServerLoop
from class_client import Client
from class_game import *
from constants import *
from class_tournament import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from asgiref.sync import sync_to_async
import secrets

#from websockets.frames import CloseCode
#from django.core.management import call_command

USERNAME_TO_GAME = {}
USERNAME_TO_CURRENTLY_QUEUING = {}
room_lock = asyncio.Lock()
connected_clients = asyncio.Queue()
background_rooms = set()

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
            client1, client2 = await connected_clients.get(), await connected_clients.get()
            client1.name, client2.name = PLAYER1, PLAYER2
            room = asyncio.create_task(NewRoom([client1, client2], DATA_LOBBY_GAME_TYPE_DUEL, None))
            background_rooms.add(room)
            room.add_done_callback(background_rooms.discard)

async def Handler(websocket):
    global connected_clients
    message = await websocket.recv()
    event = json.loads(message)

    if event[METHOD] == FROM_CLIENT:
        await HandlerClient(websocket, event)

    # if from chat_server

async def HandlerClient(websocket, event):
    client = Client(websocket, await GetUserFromToken(event[DATA_PLAYER_TOKEN]))
    # logger.debug("DEBUG:: GetUserFromToken : " + str(client.username))

    try:
        # Reconnection (or connection)
        await ConnectExpectedClient(client)
    
    	# Tournament creation?
        if (await IsUserActiveInTournament(client.username)):
            await TournamentCreatorHandler(client)
            async for message in websocket:
                event = json.loads(message)
                if (event[DATA_LOBBY_STATE] == DATA_LOBBY_ROOM_CREATED):
                    break 
            async with room_lock: game = USERNAME_TO_GAME[client.username]
            try:
                await ClientLoop(client, game, event[DATA_PLAYER])
            except Exception as e:
                logger.debug(f"An exception of type {type(e).__name__} occurred (in handler)")
                traceback.print_exc()


            
        logger.debug("HERE I CUM BACK")

        # Normal queue
        if client.username in USERNAME_TO_CURRENTLY_QUEUING:
            await AlreadyConnectedException(client)
        await connected_clients.put(client)
        USERNAME_TO_CURRENTLY_QUEUING[client.username] = True

        # Searching match
        async for message in websocket:
            event = json.loads(message)
            if (event[DATA_LOBBY_STATE] == DATA_LOBBY_ROOM_CREATED):
                break 
        async with room_lock: game = USERNAME_TO_GAME[client.username]
        try:
            del USERNAME_TO_CURRENTLY_QUEUING[client.username]
            await ClientLoop(client, game, event[DATA_PLAYER])
        except Exception as e:
            logger.debug(f"An exception of type {type(e).__name__} occurred (in handler)")
            traceback.print_exc()

	# Client left 
    except:
        await RemoveClientFromQueue(client)

async def ConnectExpectedClient(reconnecting_client):
    async with room_lock:
        if reconnecting_client.username and reconnecting_client.username in USERNAME_TO_GAME:
            game = USERNAME_TO_GAME[reconnecting_client.username]
            async with game.reconnection_lock:
                if len(game.disconnected):
                    for c in game.disconnected:
                        if (reconnecting_client.username == c.username):
                            game.disconnected.remove(c)
                            c.ws = reconnecting_client.ws 
                            game.connected.append(c)
                            try:
                                await sender.ToAll(await game.MessageBuilder.OpponentReconnected(await game.ClientsAreReady()), game.connected)
                                logger.debug("DEBUG:: found room, ready to reconnect")
                                await c.ws.send(await game.MessageBuilder.Reconnection(c, await game.ClientsAreReady()))
                                game.match_is_paused = False
                                if await game.ClientsAreReady():
                                    game.pause_time_added += (datetime.now() - game.pause_timer).total_seconds()
                                game.reconnection_lock.release()
                                room_lock.release()
                                await ClientLoop(c, game, c.name)
                            except IndexError as e :
                                logger.debug(f"List index error (in reconnection): behavior: game is canceled")
                                game.canceled = True
                                await game.TerminateModel()
                            except Exception as e:
                                logger.debug(f"An exception occurred (in reconnection): {e}")
                                traceback.print_exc()

                else:
                    room_lock.release()
                    game.reconnection_lock.release()
                    await AlreadyConnectedException(reconnecting_client)
            room_lock.release()
            game.reconnection_lock.release()

async def NewRoom(clients, game_type, tournament):
    logger.debug("DEBUG:: NewRoom() called\n")
    room_id = secrets.token_urlsafe(3)
    game = Game(room_id, clients, tournament)
    await game.CreateModel(game_type)
    clients_usernames = [clients[0].username, clients[1].username]

    for i in range(len(clients)):
        async with room_lock: USERNAME_TO_GAME[clients[i].username] = game
        logger.debug("DEBUG:: added a client to USERNAME_TO_GAME\n")
        if clients[i].ws != None:
            await clients[i].ws.send(game.MessageBuilder.NewRoomInfoFor(i, clients[i]))

    await ServerLoop(game)

    for i in range(len(clients_usernames)):
        async with room_lock: del USERNAME_TO_GAME[clients_usernames[i]]
        sys.stderr.write("DEBUG:: removed a client to USERNAME_TO_GAME\n")
 
async def RemoveClientFromQueue(client):
    try:
        del USERNAME_TO_CURRENTLY_QUEUING[client.username]
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

async def AlreadyConnectedException(client):
    await client.ws.send(json.dumps({METHOD: FROM_SERVER, OBJECT: OBJECT_INFO, DATA_INFO_TYPE: DATA_INFO_TYPE_ERROR, DATA_INFO_TYPE_ERROR: "Already present in a lobby."}));
    raise Exception("Client already present in a lobby.")

async def GetUserFromToken(token):
    access_token = AccessToken(token)
    jwt_authentication = JWTAuthentication()
    user = await sync_to_async(jwt_authentication.get_user)(access_token) 
    return user.username

async def TournamentCreatorHandler(client):
    new_tournament = Tournament() 
    await new_tournament.Init(client)
    # await ClientLoop(client, USERNAME_TO_GAME[client.username], client.name)

if __name__ == "__main__":
    asyncio.run(main())