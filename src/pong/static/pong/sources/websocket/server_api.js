import { Vec2 } from '../utils/class_vec.js';
import { NewPaddleState, NewBallState } from './objects_state.js'
import { PrintInfo } from '../ui/info.js';

// Namespace equivalent
let ServerAPI = {};

// Server messaging logic
ServerAPI.METHOD = "Method";
ServerAPI.FROM_SERVER = "FromServer"; // - FromServer
ServerAPI.FROM_CLIENT = "FromClient"; // - FromClient
ServerAPI.OBJECT = "Object";
ServerAPI.OBJECT_BALL = "Ball"; // - Ball
ServerAPI.OBJECT_PADDLE = "Paddle"; // - Paddle
ServerAPI.OBJECT_JOIN = "Join"; // - Join
ServerAPI.OBJECT_CREATE = "Create"; // - Create
ServerAPI.OBJECT_INFO = "Info";
ServerAPI.DATA_INPUT = "Input";
ServerAPI.DATA_INPUT_KEY_UP = "KeyUp";
ServerAPI.DATA_INPUT_KEY_DOWN = "KeyDown";
ServerAPI.DATA_INPUT_KEY_NONE = "None"
ServerAPI.DATA_PLAYER = "Player"
ServerAPI.DATA_PLAYER_PLAYER1 = "p1"
ServerAPI.DATA_PLAYER_PLAYER2 = "p2"
ServerAPI.DATA_JOINKEY = "JoinKey"; // - Join key
ServerAPI.DATA_POSITION = "Position";
ServerAPI.DATA_DIRECTION = "Direction";
ServerAPI.DATA_ACCELERATION = "Acceleration";
ServerAPI.DATA_INFO_TYPE = "Info_Type";
ServerAPI.DATA_INFO_TYPE_ERROR = "Error";
ServerAPI.DATA_INFO_TYPE_MESSAGE = "Message";
// Constants

// Objects state initialization
ServerAPI.player_state = null;
ServerAPI.opponent_state = null;
ServerAPI.ball_state = NewBallState();
ServerAPI.iam = "";

window.addEventListener("DOMContentLoaded", () => {
	ServerAPI.websocket = new WebSocket("ws://localhost:8888");

	// Events
	ServerAPI._InitGame();
	ServerAPI._Recv()
});

ServerAPI._InitGame = function()
{
	ServerAPI.websocket.addEventListener("open", () => {
		const params = new URLSearchParams(window.location.search);
		let event = {}
		// Joining 
		if (params.has("join")) {
			event = {	[ServerAPI.METHOD]: ServerAPI.FROM_CLIENT,
						[ServerAPI.OBJECT]: ServerAPI.OBJECT_JOIN,
						[ServerAPI.DATA_JOINKEY]: params.get("join")
			}
			ServerAPI.iam = ServerAPI.DATA_PLAYER_PLAYER2;
			ServerAPI.player_state = NewPaddleState(new Vec2(0.9, 0.));
			ServerAPI.opponent_state = NewPaddleState(new Vec2(-0.9, 0.));

		} 
		// Creating
		else {
			event = {	[ServerAPI.METHOD]: ServerAPI.FROM_CLIENT,
						[ServerAPI.OBJECT]: ServerAPI.OBJECT_CREATE
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
			default:
				console.log(event);
				break;
		}
	});
}

ServerAPI.UpdatePaddleData = function(event)
{
	if (event[ServerAPI.DATA_PLAYER] === ServerAPI.DATA_PLAYER_PLAYER1 && ServerAPI.iam === ServerAPI.DATA_PLAYER_PLAYER1) {
		ServerAPI.player_state.promise = ServerAPI.player_state.promise.then(async () => {
			ServerAPI.player_state.position = new Vec2(event[ServerAPI.DATA_POSITION][0], event[ServerAPI.DATA_POSITION][1]);
			ServerAPI.player_state.key = event[ServerAPI.DATA_INPUT];
		});
		ServerAPI.player_state.new_data_available = true;
	}
	if (event[ServerAPI.DATA_PLAYER] === ServerAPI.DATA_PLAYER_PLAYER1 && ServerAPI.iam !== ServerAPI.DATA_PLAYER_PLAYER1) {
		ServerAPI.opponent_state.promise = ServerAPI.opponent_state.promise.then(async () => {
			ServerAPI.opponent_state.position = new Vec2(event[ServerAPI.DATA_POSITION][0], event[ServerAPI.DATA_POSITION][1]);
			ServerAPI.opponent_state.key = event[ServerAPI.DATA_INPUT];
		});
		ServerAPI.opponent_state.new_data_available = true;
	}
	if (event[ServerAPI.DATA_PLAYER] === ServerAPI.DATA_PLAYER_PLAYER2 && ServerAPI.iam === ServerAPI.DATA_PLAYER_PLAYER2) {
		ServerAPI.player_state.promise = ServerAPI.player_state.promise.then(async () => {
			ServerAPI.player_state.position = new Vec2(event[ServerAPI.DATA_POSITION][0], event[ServerAPI.DATA_POSITION][1]);
			ServerAPI.player_state.key = event[ServerAPI.DATA_INPUT];
		});
		ServerAPI.player_state.new_data_available = true;
	}
	if (event[ServerAPI.DATA_PLAYER] === ServerAPI.DATA_PLAYER_PLAYER2 && ServerAPI.iam !== ServerAPI.DATA_PLAYER_PLAYER2) {
		ServerAPI.opponent_state.promise = ServerAPI.opponent_state.promise.then(async () => {
			ServerAPI.opponent_state.position = new Vec2(event[ServerAPI.DATA_POSITION][0], event[ServerAPI.DATA_POSITION][1]);
			ServerAPI.opponent_state.key = event[ServerAPI.DATA_INPUT];
		});
		ServerAPI.opponent_state.new_data_available = true;
	}
}

ServerAPI.UpdateBallData = function(event)
{
		ServerAPI.ball_state.promise = ServerAPI.ball_state.promise.then(async () => {
			ServerAPI.ball_state.position = new Vec2(event[ServerAPI.DATA_POSITION][0], event[ServerAPI.DATA_POSITION][1]);
			ServerAPI.ball_state.direction = new Vec2(event[ServerAPI.DATA_DIRECTION][0], event[ServerAPI.DATA_DIRECTION][1]);
			ServerAPI.ball_state.acceleration = event[ServerAPI.DATA_ACCELERATION];
		});
		ServerAPI.ball_state.new_data_available = true;
}

ServerAPI.GetBallState = async function()
{
	await ServerAPI.ball_state.promise;
	return { ...ServerAPI.ball_state };
}

ServerAPI.GetOpponentState = async function()
{
	await ServerAPI.opponent_state.promise;
	return { ...ServerAPI.opponent_state};
}

ServerAPI.GetPlayerState = async function()
{
	await ServerAPI.player_state.promise;
	return { ...ServerAPI.player_state};
}

ServerAPI.SendDataKey = function(key)
{
	// assert(key === ServerAPI.DATA_INPUT_KEY_UP || key === ServerAPI.DATA_INPUT_KEY_DOWN)

	const event = {
		[ServerAPI.METHOD]: ServerAPI.FROM_CLIENT,
		[ServerAPI.OBJECT]: ServerAPI.OBJECT_PADDLE,
		[ServerAPI.DATA_INPUT]: key
	}
	ServerAPI.websocket.send(JSON.stringify(event));
}

export default ServerAPI;
