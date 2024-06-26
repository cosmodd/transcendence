import { Vec2 } from '../utils/class_vec.js';
import { NewPaddleState } from './objects_state.js'
import { PrintInfo, PrintError, PrintInfoMessage } from '../ui/info.js';
import Timer from "../utils/timer.js";
import * as k from "../utils/constants_objects.js"
import { OverlayReadyButtonShow, OverlayReadyButtonHide, OverlayChangeUsernames, OverlayRefresh, OverlayShowSearching } from '../ui/overlay.js';

let ServerAPI = {};

document.addEventListener("DOMContentLoaded", function() {
    ServerAPI.InitConnection();
});

ServerAPI.InitConnection = function()
{
	ServerAPI.websocket = new WebSocket("wss://" + window.location.hostname + ":8888");

	// Events
	ServerAPI._InitGame();
	ServerAPI._Recv();
	ServerAPI._Close();
}

ServerAPI._InitGame = function()
{
	ServerAPI.websocket.addEventListener("open", async () => {
		const token = JSON.parse(localStorage.getItem("auth")).accessToken;
		let event = {
			[ServerAPI.METHOD]: ServerAPI.FROM_CLIENT,
			[ServerAPI.OBJECT]: ServerAPI.OBJECT_LOBBY,
			[ServerAPI.DATA_LOBBY_STATE]: ServerAPI.DATA_LOBBY_SEARCH,
			[ServerAPI.DATA_PLAYER_TOKEN]: token
		}
		ServerAPI.websocket.send(JSON.stringify(event));
		PrintInfoMessage("Searching for players...")
		OverlayShowSearching();
	});
}

ServerAPI._Recv = function() {
	ServerAPI.websocket.addEventListener("message", ({data}) => {
		const event = JSON.parse(data);
		if (event[ServerAPI.METHOD] != ServerAPI.FROM_SERVER)
			return ;

		if (event.hasOwnProperty(ServerAPI.DATA_TIME)) {
			Timer.ChangeRemainingTime((k.GameDuration) - Math.floor(event[ServerAPI.DATA_TIME]));
		}

		switch (event[ServerAPI.OBJECT]) {
			case ServerAPI.OBJECT_PADDLE:
				ServerAPI.UpdatePaddleData(event);
				break;
			case ServerAPI.OBJECT_BALL:
				ServerAPI.UpdateBallData(event);
				break;
			case ServerAPI.OBJECT_INFO:
				PrintInfo(event);
				break ;
			case ServerAPI.OBJECT_LOBBY:
				ServerAPI.UpdateLobby(event);
				break ;
			default:
				console.log(event);
				break;
		}
	});
}

ServerAPI._Close = function()
{
	ServerAPI.websocket.addEventListener("close", (event) => {
		switch (event.code) {
			case 1006:
				PrintError("Connection closed: Abnormal Closure");
				break;
			default:
				// PrintError(event.reason);	
				break;
		}
	});
}

ServerAPI.UpdatePaddleData = function(event)
{
	let paddle_state = 
		ServerAPI.iam === event[ServerAPI.DATA_PLAYER] ? 
			ServerAPI.player_state :
			ServerAPI.opponent_state;

	if (paddle_state === null)
		return ;

	paddle_state.promise = paddle_state.promise.then(async () => {
		paddle_state.position.SetXY(event[ServerAPI.DATA_POSITION][0], event[ServerAPI.DATA_POSITION][1]);
		paddle_state.key = event[ServerAPI.DATA_INPUT];
		paddle_state.new_data_available = true;
	});
}

ServerAPI.UpdateBallData = function(event)
{
	ServerAPI.ball_state.promise = ServerAPI.ball_state.promise.then(async () => {
		ServerAPI.ball_state.position.SetXY(event[ServerAPI.DATA_POSITION][0], event[ServerAPI.DATA_POSITION][1]);
		ServerAPI.ball_state.direction.SetXY(event[ServerAPI.DATA_DIRECTION][0], event[ServerAPI.DATA_DIRECTION][1]);
		ServerAPI.ball_state.acceleration = event[ServerAPI.DATA_ACCELERATION];
		ServerAPI.ball_state.new_data_available = true;
	});
}

ServerAPI.UpdateLobby = function(event)
{
	if (event.hasOwnProperty(ServerAPI.DATA_LOBBY_STATE))
		ServerAPI.UpdateLobbyState(event)

	if (event.hasOwnProperty(ServerAPI.DATA_LOBBY_SCORE)) {
		let score = event[ServerAPI.DATA_LOBBY_SCORE];
		ServerAPI.score_state.promise = ServerAPI.score_state.promise.then(async () => {
			ServerAPI.score_state.score[ServerAPI.DATA_PLAYER_PLAYER1] = score[0];
			ServerAPI.score_state.score[ServerAPI.DATA_PLAYER_PLAYER2] = score[1];
			ServerAPI.ball_state.new_data_available = true;
		});
	}
}

ServerAPI.UpdateLobbyState = function(event)
{
	switch (event[ServerAPI.DATA_LOBBY_STATE]) {
		// Room created
		case ServerAPI.DATA_LOBBY_ROOM_CREATED:
			ServerAPI.UpdateLobbyStateRoomCreated(event);
			break ;
		// Both players are ready
		case ServerAPI.DATA_PLAYER_READY:
			ServerAPI.UpdateLobbyStateRoomStarted(event);
			break;
		// Room ended
		case ServerAPI.DATA_LOBBY_ROOM_ENDED:
			ServerAPI.UpdateLobbyStateRoomEnded(event);
			break ;
		// Match paused
		case ServerAPI.DATA_LOBBY_ROOM_PAUSED:
			Timer.Pause();
			PrintInfo(event);
			break ;
		// Reconnection
		case ServerAPI.DATA_LOBBY_ROOM_RECONNECTED:
			ServerAPI.UpdateLobbyStateRoomReconnected(event);
			break ;
		default:
			PrintInfo(event);
			break ;
	}
}

ServerAPI.UpdateLobbyStateRoomCreated = function(event)
{
	ServerAPI.iam = event[ServerAPI.DATA_PLAYER];
	OverlayReadyButtonShow(event[ServerAPI.DATA_LOBBY_GAME_TYPE], event[ServerAPI.DATA_OPPONENT_USERNAME]);
	console.log(event[ServerAPI.DATA_OPPONENT_USERNAME]);
	OverlayChangeUsernames(event[ServerAPI.DATA_OPPONENT_USERNAME], ServerAPI.iam);
	let response_create = {
		[ServerAPI.METHOD]: ServerAPI.FROM_CLIENT,
		[ServerAPI.OBJECT]: ServerAPI.OBJECT_LOBBY,
		[ServerAPI.DATA_LOBBY_STATE]: ServerAPI.DATA_LOBBY_ROOM_CREATED,
		[ServerAPI.DATA_PLAYER]: ServerAPI.iam,
		[ServerAPI.DATA_LOBBY_ROOM_ID]: event[ServerAPI.DATA_LOBBY_ROOM_ID]
	}
	ServerAPI.websocket.send(JSON.stringify(response_create));
	PrintInfo(event);
}


ServerAPI.UpdateLobbyStateRoomStarted = function(event)
{
	ServerAPI.player_state = (ServerAPI.iam === ServerAPI.DATA_PLAYER_PLAYER1) ? NewPaddleState(new Vec2(-0.9, 0.)) : NewPaddleState(new Vec2(0.9, 0.));
	ServerAPI.opponent_state = (ServerAPI.iam === ServerAPI.DATA_PLAYER_PLAYER1) ? NewPaddleState(new Vec2(0.9, 0.)) : NewPaddleState(new Vec2(-0.9, 0.));
	Timer.Start(k.GameDuration);
	PrintInfo(event);
}

ServerAPI.UpdateLobbyStateRoomEnded = function(event)
{
	let response_end = {
		[ServerAPI.METHOD]: ServerAPI.FROM_CLIENT,
		[ServerAPI.OBJECT]: ServerAPI.OBJECT_LOBBY,
		[ServerAPI.DATA_LOBBY_STATE]: ServerAPI.DATA_LOBBY_ROOM_ENDED,
	}
	ServerAPI.websocket.send(JSON.stringify(response_end));
	PrintInfo(event);
}

ServerAPI.UpdateLobbyStateRoomReconnected = function(event)
{
	OverlayRefresh();

	if (event.hasOwnProperty(ServerAPI.DATA_PLAYER)) {
		ServerAPI.iam = event[ServerAPI.DATA_PLAYER];
		ServerAPI.player_state = (ServerAPI.iam === ServerAPI.DATA_PLAYER_PLAYER1) ? NewPaddleState(new Vec2(-0.9, 0.)) : NewPaddleState(new Vec2(0.9, 0.));
		ServerAPI.opponent_state = (ServerAPI.iam === ServerAPI.DATA_PLAYER_PLAYER1) ? NewPaddleState(new Vec2(0.9, 0.)) : NewPaddleState(new Vec2(-0.9, 0.));
		OverlayChangeUsernames(event[ServerAPI.DATA_OPPONENT_USERNAME], ServerAPI.iam);
	}

	if (event[ServerAPI.DATA_LOBBY_BOTH_ARE_READY] === true)
		Timer.Start();

	if (event[ServerAPI.DATA_PLAYER_STATE] == ServerAPI.DATA_PLAYER_READY) {
		OverlayReadyButtonHide()
	}
	else {
		if (event.hasOwnProperty(ServerAPI.DATA_LOBBY_GAME_TYPE)) {
			OverlayChangeUsernames(event[ServerAPI.DATA_OPPONENT_USERNAME], ServerAPI.iam);
			OverlayReadyButtonShow(event[ServerAPI.DATA_LOBBY_GAME_TYPE], event[ServerAPI.DATA_OPPONENT_USERNAME]);
		}
	}

	PrintInfo(event);
}

ServerAPI.SendReadyState = function()
{
	let message = {
		[ServerAPI.METHOD]: ServerAPI.FROM_CLIENT,
		[ServerAPI.DATA_PLAYER_STATE]: ServerAPI.DATA_PLAYER_READY
	}
	ServerAPI.websocket.send(JSON.stringify(message));
}

export default ServerAPI;