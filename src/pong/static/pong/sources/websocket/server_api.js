import { Vec2 } from '../utils/class_vec.js';

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
ServerAPI.DATA_INPUT = "Input";
ServerAPI.DATA_INPUT_KEY_UP = "KeyUp";
ServerAPI.DATA_INPUT_KEY_DOWN = "KeyDown";
ServerAPI.DATA_INPUT_KEY_NONE = "None"
ServerAPI.DATA_PLAYER = "Player"
ServerAPI.DATA_PLAYER_PLAYER1 = "p1"
ServerAPI.DATA_PLAYER_PLAYER2 = "p2"
ServerAPI.DATA_JOINKEY = "JoinKey"; // - Join key
ServerAPI.DATA_POSITION = "Position"; // - Data position

ServerAPI.self_pos_promise = Promise.resolve();
ServerAPI.self_key_promise = Promise.resolve();
ServerAPI.self_pos = new Vec2(-0.9, 0.);
ServerAPI.self_key = ServerAPI.DATA_INPUT_KEY_NONE
ServerAPI.self_new_data = false;
ServerAPI.opp_pos_promise = Promise.resolve();
ServerAPI.opp_key_promise = Promise.resolve();
ServerAPI.opp_pos = new Vec2(0.9, 0.);
ServerAPI.opp_key = ServerAPI.DATA_INPUT_KEY_NONE
ServerAPI.opp_new_data = false;
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
		} 
		// Creating
		else {
			event = {	[ServerAPI.METHOD]: ServerAPI.FROM_CLIENT,
						[ServerAPI.OBJECT]: ServerAPI.OBJECT_CREATE
			}
			ServerAPI.iam = ServerAPI.DATA_PLAYER_PLAYER1;
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
			default:
				// throw new Error(`Unsupported event type: ${event.type}.`);
				console.log(event);
		}
	});
}

ServerAPI.UpdatePaddleData = function(event)
{
	if (event[ServerAPI.DATA_PLAYER] === ServerAPI.DATA_PLAYER_PLAYER1 && ServerAPI.iam === ServerAPI.DATA_PLAYER_PLAYER1) {
		ServerAPI.self_pos_promise = ServerAPI.self_pos_promise.then(async () => {
			ServerAPI.self_pos = new Vec2(event[ServerAPI.DATA_POSITION][0], event[ServerAPI.DATA_POSITION][1])});
		ServerAPI.self_key_promise = ServerAPI.self_key_promise.then(async () => {
			ServerAPI.self_key = event[ServerAPI.DATA_INPUT]});
		ServerAPI.self_new_data = true;
	}
	if (event[ServerAPI.DATA_PLAYER] === ServerAPI.DATA_PLAYER_PLAYER1 && ServerAPI.iam !== ServerAPI.DATA_PLAYER_PLAYER1) {
		ServerAPI.opp_pos_promise = ServerAPI.opp_pos_promise.then(async () => {
				ServerAPI.opp_pos = new Vec2(event[ServerAPI.DATA_POSITION][0], event[ServerAPI.DATA_POSITION][1])});
		ServerAPI.opp_key_promise = ServerAPI.opp_key_promise.then(async () => {
			ServerAPI.opp_key = event[ServerAPI.DATA_INPUT]});
		ServerAPI.opp_new_data = true;
	}
	if (event[ServerAPI.DATA_PLAYER] === ServerAPI.DATA_PLAYER_PLAYER2 && ServerAPI.iam === ServerAPI.DATA_PLAYER_PLAYER2) {
		ServerAPI.self_pos_promise = ServerAPI.self_pos_promise.then(async () => {
			ServerAPI.self_pos = new Vec2(event[ServerAPI.DATA_POSITION][0], event[ServerAPI.DATA_POSITION][1])});
		ServerAPI.self_key_promise = ServerAPI.self_key_promise.then(async () => {
			ServerAPI.self_key = event[ServerAPI.DATA_INPUT]});
		ServerAPI.self_new_data = true;
	}
	if (event[ServerAPI.DATA_PLAYER] === ServerAPI.DATA_PLAYER_PLAYER2 && ServerAPI.iam !== ServerAPI.DATA_PLAYER_PLAYER2) {
		ServerAPI.opp_pos_promise = ServerAPI.opp_pos_promise.then(async () => {
				ServerAPI.opp_pos = new Vec2(event[ServerAPI.DATA_POSITION][0], event[ServerAPI.DATA_POSITION][1])});
		ServerAPI.opp_key_promise = ServerAPI.opp_key_promise.then(async () => {
			ServerAPI.opp_key = event[ServerAPI.DATA_INPUT]});
		ServerAPI.opp_new_data = true;
	}
}

ServerAPI.GetPositionOpponent = async function()
{
	await ServerAPI.opp_pos_promise;
	let ret = ServerAPI.opp_pos.Clone();
	ret.x *= -1.0;
	return ret;
}

ServerAPI.GetPositionPlayer = async function()
{
	await ServerAPI.self_pos_promise;
	return ServerAPI.self_pos.Clone();
}

ServerAPI.GetKeyPlayer = async function()
{
	await ServerAPI.self_key_promise;
	return ServerAPI.self_key;
}

ServerAPI.GetKeyOpponent = async function()
{
	await ServerAPI.opp_key_promise;
	return ServerAPI.opp_key;
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
