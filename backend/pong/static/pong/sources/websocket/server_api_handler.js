import { Vec2 } from '../utils/class_vec.js';
import { NewPaddleState } from './objects_state.js'
import { PrintInfo, PrintError, PrintInfoMessage } from '../ui/info.js';
import { SetCookie, DeleteCookie, GetCookie } from '../utils/cookie.js'
import Timer from "../utils/timer.js";
import * as k from "../utils/constants_objects.js"

let ServerAPI = {};

ServerAPI.InitConnection = function()
{
	ServerAPI.websocket = new WebSocket("ws://" + window.location.hostname + ":8888");

	// Events
	ServerAPI._InitGame();
	ServerAPI._Recv();
	ServerAPI._Close();
}

ServerAPI._InitGame = function()
{
	ServerAPI.websocket.addEventListener("open", () => {
		let event = {
			[ServerAPI.METHOD]: ServerAPI.FROM_CLIENT,
			[ServerAPI.OBJECT]: ServerAPI.OBJECT_LOBBY,
			[ServerAPI.DATA_LOBBY_STATE]: ServerAPI.DATA_LOBBY_SEARCH,
			[ServerAPI.DATA_PLAYER_TOKEN]: JSON.parse(localStorage.getItem("auth")).accessToken,
			[ServerAPI.DATA_LOBBY_ROOM_ID]: GetCookie("pong-roomid")
			//localstorage.getitem("auth").accessToken
		}
		ServerAPI.websocket.send(JSON.stringify(event));
		PrintInfoMessage("Searching for players...")
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
				PrintError("Connection closed: 1006: Abnormal Closure");
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
		// Room ended
		case ServerAPI.DATA_LOBBY_ROOM_ENDED:
			ServerAPI.UpdateLobbyStateRoomEnded(event);
			break ;
		// Match paused
		case ServerAPI.DATA_LOBBY_ROOM_PAUSED:
			Timer.Pause();
			break ;
		// Reconnection
		case ServerAPI.DATA_LOBBY_ROOM_RECONNECTED:
			Timer.Start()
			PrintInfo(event);
			break ;
		default:
			PrintInfo(event);
			break ;
	}
}

ServerAPI.UpdateLobbyStateRoomCreated = function(event)
{
	ServerAPI.iam = event[ServerAPI.DATA_PLAYER];
	ServerAPI.player_state = (ServerAPI.iam === ServerAPI.DATA_PLAYER_PLAYER1) ? NewPaddleState(new Vec2(-0.9, 0.)) : NewPaddleState(new Vec2(0.9, 0.));
	ServerAPI.opponent_state = (ServerAPI.iam === ServerAPI.DATA_PLAYER_PLAYER1) ? NewPaddleState(new Vec2(0.9, 0.)) : NewPaddleState(new Vec2(-0.9, 0.));
	SetCookie("pong-roomid", event[ServerAPI.DATA_LOBBY_ROOM_ID]);
	let response_create = {
		[ServerAPI.METHOD]: ServerAPI.FROM_CLIENT,
		[ServerAPI.OBJECT]: ServerAPI.OBJECT_LOBBY,
		[ServerAPI.DATA_LOBBY_STATE]: ServerAPI.DATA_LOBBY_ROOM_CREATED,
		[ServerAPI.DATA_PLAYER]: ServerAPI.iam,
		[ServerAPI.DATA_LOBBY_ROOM_ID]: event[ServerAPI.DATA_LOBBY_ROOM_ID]
	}
	ServerAPI.websocket.send(JSON.stringify(response_create));
	PrintInfo(event);
	Timer.Start(k.GameDuration);
}

ServerAPI.UpdateLobbyStateRoomEnded = function(event)
{
	DeleteCookie("pong-uuid");
	DeleteCookie("pong-roomid");
	let response_end = {
		[ServerAPI.METHOD]: ServerAPI.FROM_CLIENT,
		[ServerAPI.OBJECT]: ServerAPI.OBJECT_LOBBY,
		[ServerAPI.DATA_LOBBY_STATE]: ServerAPI.DATA_LOBBY_ROOM_ENDED,
	}
	ServerAPI.websocket.send(JSON.stringify(response_end));
	PrintInfo(event);
}

export default ServerAPI;