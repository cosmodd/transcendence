import json
import websockets
from class_pong import *
from constants import *
from datetime import datetime
import asyncio

async def SendToAll(dumped_message, connected):
    # websockets.broadcast(connected, dumped_message)
    for ws in connected:
        await ws.send(dumped_message)


async def StateLoop(game: Pong, connected):
    last_update_time = datetime.now()
    while (True):
        current_time = datetime.now()
        delta_time = (current_time - last_update_time).total_seconds()
        last_update_time = current_time

        # Update positions
        game.UpdatePosition(PLAYER1, delta_time)
        game.UpdatePosition(PLAYER2, delta_time)

        # Collisions

        # Send game state to clients
        # Only if player changed key
        if  (game._players[PLAYER1].has_key_changed):
            player1_message = game.MessageBuilder.Paddle(PLAYER1)
            await SendToAll(player1_message, connected)
            game._players[PLAYER1].has_key_changed = False

        if  (game._players[PLAYER2].has_key_changed):
            player2_message = game.MessageBuilder.Paddle(PLAYER2)
            await SendToAll(player2_message, connected)
            game._players[PLAYER2].has_key_changed = False

        await asyncio.sleep(0.01) 


async def Play(websocket, game: Pong, current_player, connected):
    async for message in websocket:
        try:
            event = json.loads(message)
            assert event[METHOD] == FROM_CLIENT

            # Receive key from player
            if event[OBJECT] == OBJECT_PADDLE:
                game.RegisterKeyInput(current_player, event.get(DATA_INPUT))

        except json.JSONDecodeError:
            print("Error decoding JSON message.")
        except KeyError as e:
            print(f"KeyError: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
 