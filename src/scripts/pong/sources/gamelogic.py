import json
import websockets
import collision
import sender
from class_game import *
from constants import *
from datetime import datetime
import asyncio

async def ServerSendLoop(game: Game, connected):
    last_update_time = datetime.now()
    # temporary
    game._ball.Reset()
    game._ball.collided = True
    while (True):
        # Check disconnection
        await CaDecoOuuu(connected);

        # Delta time
        current_time = datetime.now()
        delta_time = (current_time - last_update_time).total_seconds()
        last_update_time = current_time

        # Update positions
        game.UpdatePaddlePosition(PLAYER1, delta_time)
        game.UpdatePaddlePosition(PLAYER2, delta_time)
        game.UpdateBallPosition(delta_time)

        # Collisions
        collision.PaddleWall(game._players[PLAYER1])
        collision.PaddleWall(game._players[PLAYER2])
        collision.Ball(game._ball, game._players[PLAYER1], game._players[PLAYER2], delta_time)
        # collision.BallWall(game._ball)
        # collision.BallPaddle(game._ball, game._players[PLAYER1])
        # collision.BallPaddle(game._ball, game._players[PLAYER2])

        # Send game state to clients [only if:]
            # Client changed key
            # Ball collided
        if  (game._players[PLAYER1].key_has_changed):
            player1_message = game.MessageBuilder.Paddle(PLAYER1)
            await sender.ToAll(player1_message, connected)
            game._players[PLAYER1].key_has_changed = False

        if  (game._players[PLAYER2].key_has_changed):
            player2_message = game.MessageBuilder.Paddle(PLAYER2)
            await sender.ToAll(player2_message, connected)
            game._players[PLAYER2].key_has_changed = False

        if (game._ball.collided):
            ball_message = game.MessageBuilder.Ball()
            await sender.ToAll(ball_message, connected)
            game._ball.collided = False

        await asyncio.sleep(0.01) 


async def ClientRecvLoop(websocket, game: Game, current_player, connected):
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
            print(f"An unexpected Error occurred: {e}")
 
async def CaDecoOuuu(connected):
    # Check if any client has disconnected
    disconnected_clients = []
    for ws in connected:
        if ws.closed:
            disconnected_clients.append(ws)
    # Remove disconnected clients from the connected list
    for ws in disconnected_clients:
        connected.remove(ws)
    
    # Send disconnection message
    for ws in disconnected_clients:
        for wsc in connected:
            await sender.Error(wsc, "Opponent disconnected.")
