import json
import websockets
from pong import Pong

async def play(websocket, game, current_player, connected):
    async for message in websocket:
        try:
            event = json.loads(message)

            # Receive data and transmit to the other - temporary
            if event["type"] == "send" and event["object"] == "paddle":
                position = game.AssertNewPlayerPosition(current_player, event.get("position"))
                paddle_data = {
                    "type": "get",
                    "object": "paddle",
                    "position": [position[0], position[1]]
                }
                for ws in connected:
                    if ws != websocket:
                        await ws.send(json.dumps(paddle_data))

        except json.JSONDecodeError:
            print("Error decoding JSON message.")
        except KeyError as e:
            print(f"KeyError: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
 