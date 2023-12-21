import json
import websockets
from class_pong import Pong
from constants import *
from datetime import datetime

async def SendToAll(dumped_message, connected):
    # websockets.broadcast(connected, dumped_message)
    for ws in connected:
        await ws.send(dumped_message)


last_update_time = datetime.now()
async def StateLoop(game: Pong, connected):
    while (True):
        current_time = datetime.now()
        delta_time = (current_time - last_update_time).total_seconds()
        last_update_time = current_time

        # Update positions
        game.UpdatePosition(PLAYER1, delta_time)
        game.UpdatePosition(PLAYER2, delta_time)

        # Collisions

        # Send game state to clients
        player1_message = game.MessageBuilder.PlayerPosition(PLAYER1)
        await SendToAll(player1_message, connected)
        player2_message = game.MessageBuilder.PlayerPosition(PLAYER2)
        await SendToAll(player2_message, connected)


async def Play(websocket, game: Pong, current_player, connected):
    asyncio.ensure_future(StateLoop(game, connected))

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
 