import json
import asyncio
from datetime import datetime
import sender as sender
from class_game import *
from class_client import *
from constants import *
from class_vec2 import Vec2
from constants import *
import traceback
import sys

SLEEPING_TIME = 1 / 120

async def ClientLoop(client: Client, game: Game, current_player):
    # Client lobby ready loop
    if await client.IsReady() == False:
        async for message in client.ws:
            event = json.loads(message)
            assert event[METHOD] == FROM_CLIENT
            if DATA_PLAYER_STATE in event:
                if event[DATA_PLAYER_STATE] == DATA_PLAYER_READY:
                    await client.SetReadyState(True)
                    break 

    if client.ws.closed:
        await HandleDisconnection(game)
        return

    # Client game loop
    async for message in client.ws:
        event = json.loads(message)
        # sys.stderr.write("Receive in ClientLoop: " + message + "\n")
        assert event[METHOD] == FROM_CLIENT

        # Receive key from player
        if OBJECT in event:
            if event[OBJECT] == OBJECT_PADDLE:
                game.RegisterKeyInput(current_player, event.get(DATA_INPUT))
            # Game ended
            if event[OBJECT] == OBJECT_LOBBY:
                if event[DATA_LOBBY_STATE] == DATA_LOBBY_ROOM_ENDED:
                    return

    if client.ws.closed:
        await HandleDisconnection(game)

async def ServerLoop(game: Game):
    sys.stderr.write("DEBUG:: ServerLoop created\n")
    try:
        game.start_time = datetime.now()
        while await game.ClientsAreReadyAndConnected() == False:
            if await game.OneOfClientsIsConnected():
                game.start_time = datetime.now()
            if (datetime.now() - game.start_time).total_seconds() >= 30:
                raise Exception("Lobby waiting time expired")
            await asyncio.sleep(1)

        game.ball.Reset(Vec2(-1., 0.))
        game.ball.collided = True
        game.match_is_running = True
        last_update_time = datetime.now()
        game.start_time = datetime.now()

        for i in range(len(game.clients)):
            await game.clients[i].ws.send(game.MessageBuilder.ClientsAreReady(i))

        sys.stderr.write("DEBUG:: Beginning game\n")
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
                await sender.ToAll(game.MessageBuilder.Paddle(PLAYER1), game.connected)
                await sender.ToAll(game.MessageBuilder.Paddle(PLAYER2), game.connected)
                game.someone_scored = False
                game.match_is_running = IsScoreLimitNotReached(game) and IsTimeNotExpired(game)
                if (game.match_is_running == False):
                    game.match_is_running = ScoreIsEven(game)

            # Game paused
            while game.IsMatchPaused() or game.ClientsAreReady == False:
                async with game.reconnection_lock: await LastPlayerDisconnection(game);
                await sender.ToAll(game.MessageBuilder.PausedGame(), game.connected)
                await sender.ToAll(game.MessageBuilder.FreezeBall(), game.connected)
                await asyncio.sleep(1)

            await asyncio.sleep(SLEEPING_TIME) 
        await game.TerminateModel()
        game.StopBall()
        await sender.ToAll(game.MessageBuilder.Ball(), game.connected)
        await sender.ToAll(game.MessageBuilder.EndGame(), game.connected)

    except Exception as e:
        game.cancelled = True
        await game.TerminateModel()
        traceback.print_exc()
 
async def HandleDisconnection(game: Game):
    old_disconnected = game.disconnected

    # Check if any client has disconnected
    newly_disconnected = [c for c in game.connected if c.ws.closed]

    # Removing disconnected clients from connected list
    for c in newly_disconnected:
        game.connected.remove(c)

	# Keeping clients that didnt connected a single time
    not_connected_yet = [c for c in game.disconnected if c.ws == None] 

    game.disconnected = newly_disconnected + not_connected_yet + old_disconnected

    # Both connected
    if (len(game.connected) == 2):
        return 
    # Both disconnected
    if (len(game.connected) == 0):
        game.match_is_running = False
        game.match_is_paused = False
        game.cancelled = True
        return 
    # One disconnection
    if (len(game.connected) == 1 and game.match_is_running):
        game.match_is_paused = True
        game.pause_timer = datetime.now()
    # Send disconnection message
    for c in newly_disconnected:
        for cc in game.connected:
            if not cc.ws.closed:
                await sender.Error(cc.ws, "Opponent disconnected.")

async def LastPlayerDisconnection(game: Game):
    # Reconnection happened
    if len(game.connected) == 2:
        return
    # Check if last client disconnected
    for c in game.connected:
        if c.ws.closed:
            game.match_is_running = False
            game.match_is_paused = False
            game.cancelled = True
    # Reconnection timeout
    if ((datetime.now() - game.pause_timer).total_seconds() >= kReconnectionWaitingTime):
        game.match_is_running = False
        game.match_is_paused = False
        game.game_ended_with_timeout = True

def IsScoreLimitNotReached(game: Game):
    return (game.score[PLAYER1].score < kScoreLimit and game.score[PLAYER2].score < kScoreLimit)

def IsTimeNotExpired(game: Game):
    return ((datetime.now() - game.start_time).total_seconds() < float(kGameDuration + game.pause_time_added))

def ScoreIsEven(game: Game):
    return (game.score[PLAYER1].score == game.score[PLAYER2].score)
