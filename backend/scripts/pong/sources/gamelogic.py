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

async def ClientLoop(websocket, game: Game, current_player):
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

async def ServerLoop(game: Game):
    last_update_time = datetime.now()
    game.ball.Reset(Vec2(-1., 0.))
    game.ball.collided = True
    while (game.IsMatchRunning()):

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
            await sender.ToAll(game.MessageBuilder.Paddle(PLAYER1), game.connected)
            game.players[PLAYER1].key_has_changed = False

        if  (game.players[PLAYER2].key_has_changed):
            await sender.ToAll(game.MessageBuilder.Paddle(PLAYER2), game.connected)
            game.players[PLAYER2].key_has_changed = False

        if (game.ball.collided):
            await sender.ToAll(game.MessageBuilder.Ball(), game.connected)
            game.ball.collided = False

        if (game.someone_scored):
            await sender.ToAll(game.MessageBuilder.Score(), game.connected)
            game.someone_scored = False

        # Check disconnection
        await Deconnection(game);

        # Game paused
        while game.IsMatchPaused():
            await LastPlayerDeconnection(game);
            await sender.ToAll(game.MessageBuilder.PausedGame(), game.connected)
            await asyncio.sleep(1)

        await asyncio.sleep(1 / 60) 
    await game.TerminateModel()
    await sender.ToAll(game.MessageBuilder.EndGame(), game.connected)
 
async def Deconnection(game: Game):
    newly_disconnected = [c for c in game.connected if c.ws.closed]
    # Check if any client has disconnected
    for c in newly_disconnected:
        game.connected.remove(c)
    # end match ?
    if (len(game.connected) == 0):
        game.match_is_running = False
        game.match_is_paused = False
    if (len(game.connected) == 1):
        game.match_is_paused = True
    # Send disconnection message
    for c in newly_disconnected:
        for cc in game.connected:
            await sender.Error(cc.ws, "Opponent disconnected.")
    game.disconnected = newly_disconnected

async def LastPlayerDeconnection(game: Game):
    # Reconnection happened
    if len(game.connected) == 2:
        return
    # Check if last client disconnected
    for c in game.connected:
        if c.ws.closed:
            game.match_is_running = False
            game.match_is_paused = False

