import json
import websockets
from class_pong import Pong
from constants import *

async def SendToOpponent(dumped_message, websocket, connected):
    for ws in connected:
        if ws != websocket:
            await ws.send(dumped_message)

async def play(websocket, game, current_player, connected):
    async for message in websocket:
        try:
            event = json.loads(message)
            assert event[METHOD] == FROM_CLIENT

            # Receive data and transmit to the other - temporary
            if event[OBJECT] == OBJECT_PADDLE:
                game.ActualizePlayerPosition(current_player, event.get(DATA_POSITION))
                paddle_data_message = game.MessageBuilder.PlayerPosition(current_player)
                await SendToOpponent(paddle_data_message, websocket, connected)

        except json.JSONDecodeError:
            print("Error decoding JSON message.")
        except KeyError as e:
            print(f"KeyError: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
 