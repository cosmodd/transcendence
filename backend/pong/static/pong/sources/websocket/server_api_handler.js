import ServerAPI from "./server_api.js";
import { Vec2 } from '../utils/class_vec.js';
import { NewPaddleState, NewBallState } from './objects_state.js'
import { PrintInfo, PrintError } from '../ui/info.js';

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
		const params = new URLSearchParams(window.location.search);
		let event = {}
		// Joining 
		if (params.has("join")) {
			event = {	[ServerAPI.METHOD]: ServerAPI.FROM_CLIENT,
						[ServerAPI.OBJECT]: ServerAPI.OBJECT_LOBBY,
						[ServerAPI.DATA_LOBBY_STATE]: ServerAPI.DATA_LOBBY_JOIN,
						[ServerAPI.DATA_LOBBY_JOINKEY]: params.get("join")
			}
			ServerAPI.iam = ServerAPI.DATA_PLAYER_PLAYER2;
			ServerAPI.player_state = NewPaddleState(new Vec2(0.9, 0.));
			ServerAPI.opponent_state = NewPaddleState(new Vec2(-0.9, 0.));

		} 
		// Creating
		else {
			event = {	[ServerAPI.METHOD]: ServerAPI.FROM_CLIENT,
						[ServerAPI.OBJECT]: ServerAPI.OBJECT_LOBBY,
						[ServerAPI.DATA_LOBBY_STATE]: ServerAPI.DATA_LOBBY_CREATE
			}
			ServerAPI.iam = ServerAPI.DATA_PLAYER_PLAYER1;
			ServerAPI.player_state = NewPaddleState(new Vec2(-0.9, 0.));
			ServerAPI.opponent_state = NewPaddleState(new Vec2(0.9, 0.));
		}
		ServerAPI.websocket.send(JSON.stringify(event));
	});
}

ServerAPI._Recv = function() {
	ServerAPI.websocket.addEventListener("message", ({data}) => {
		const event = JSON.parse(data);

		if (event[ServerAPI.METHOD] != ServerAPI.FROM_SERVER)
			return ;

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
	let score = event[ServerAPI.DATA_LOBBY_SCORE];
	ServerAPI.score_state.promise = ServerAPI.score_state.promise.then(async () => {
		ServerAPI.score_state.score[ServerAPI.DATA_PLAYER_PLAYER1] = score[0];
		ServerAPI.score_state.score[ServerAPI.DATA_PLAYER_PLAYER2] = score[1];
		ServerAPI.ball_state.new_data_available = true;
	});
}
