import json
import websockets
import scripts.pong.sources.class_collision as class_collision
import sender
from class_game import *
from class_client import *
from constants import *
from datetime import datetime
from class_vec2 import Vec2
import asyncio


async def ServerSendLoop(game: Game, connected):
    last_update_time = datetime.now()
    game.ball.Reset(Vec2(-1., 0.))
    game.ball.collided = True
    while (game.IsMatchRunning()):
        # Check disconnection
        await CaDecoOuuu(connected, game);

        # Delta time
        current_time = datetime.now()
        delta_time = (current_time - last_update_time).total_seconds()
        last_update_time = current_time

        # Update positions
        game.UpdatePaddlePosition(PLAYER1, delta_time)
        game.UpdatePaddlePosition(PLAYER2, delta_time)
        game.UpdateBallPosition(delta_time)

        # Collisions
        game.Collision.PaddleWall(game.players[PLAYER1])
        game.Collision.PaddleWall(game.players[PLAYER2])
        game.Collision.BallPaddle(game.ball, game.players[PLAYER1])
        game.Collision.BallPaddle(game.ball, game.players[PLAYER2])
        if game.ball.collided == False:
            await game.Collision.BallWall(game.ball)

        # Send game state to clients [only if:]
        if  (game.players[PLAYER1].key_has_changed):
            player1_message = game.MessageBuilder.Paddle(PLAYER1)
            await sender.ToAll(player1_message, connected)
            game.players[PLAYER1].key_has_changed = False

        if  (game.players[PLAYER2].key_has_changed):
            player2_message = game.MessageBuilder.Paddle(PLAYER2)
            await sender.ToAll(player2_message, connected)
            game.players[PLAYER2].key_has_changed = False

        if (game.ball.collided):
            ball_message = game.MessageBuilder.Ball()
            await sender.ToAll(ball_message, connected)
            game.ball.collided = False

        if (game.someone_scored):
            score_message = game.MessageBuilder.Score()
            await sender.ToAll(score_message, connected)
            game.someone_scored = False

        await asyncio.sleep(1 / 60) 
    await game.TerminateModel()


async def ClientRecvLoop(websocket, game: Game, current_player):
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
 
async def CaDecoOuuu(connected, game: Game):
    disconnected_clients = []
    # Check if any client has disconnected
    for c in connected:
        if c.ws.closed:
            disconnected_clients.append(c)
    # Remove disconnected clients from the connected list
    for c in disconnected_clients:
        connected.remove(c)
    # Is everybody out ?
    if (len(connected) != 2):
        game.match_is_running = False
    # Send disconnection message
    for c in disconnected_clients:
        for cc in connected:
            await sender.Error(cc.ws, "Opponent disconnected.")
