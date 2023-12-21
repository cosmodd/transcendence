//  Game logic events
const METHOD = "Method";
	const FROM_SERVER = "FromServer"; // - FromServer
	const FROM_CLIENT = "FromClient"; // - FromClient
const OBJECT = "Object";
	const OBJECT_BALL = "Ball"; // - Ball
	const OBJECT_PADDLE = "Paddle"; // - Paddle
	const OBJECT_JOIN = "Join"; // - Join
	const OBJECT_CREATE = "Create"; // - Create
//	 Data
const DATA_INPUT = "Input";
	const DATA_INPUT_KEY_UP = "KeyUp";
	const DATA_INPUT_KEY_DOWN = "KeyDown";
	const DATA_INPUT_KEY_NONE = "None"
const DATA_PLAYER = "Player"
	const DATA_PLAYER_PLAYER1 = "p1"
	const DATA_PLAYER_PLAYER2 = "p2"
const DATA_JOINKEY = "JoinKey"; // - Join key
const DATA_POSITION = "Position"; // - Data position

import { Vec2 } from '../utils/class_vec.js';


// Namespace equivalent
let ServerAPI = {};

ServerAPI.self_pos_promise = Promise.resolve();
ServerAPI.self_key_promise = Promise.resolve();
ServerAPI.self_pos = new Vec2(-0.9, 0.);
ServerAPI.self_key = DATA_INPUT_KEY_NONE
ServerAPI.self_new_data = false;
ServerAPI.opp_pos_promise = Promise.resolve();
ServerAPI.opp_key_promise = Promise.resolve();
ServerAPI.opp_pos = new Vec2(0.9, 0.);
ServerAPI.opp_key = DATA_INPUT_KEY_NONE
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
			event = {	[METHOD]: FROM_CLIENT,
						[OBJECT]: OBJECT_JOIN,
						[DATA_JOINKEY]: params.get("join")
			}
			ServerAPI.iam = DATA_PLAYER_PLAYER2;
		} 
		// Creating
		else {
			event = {	[METHOD]: FROM_CLIENT,
						[OBJECT]: OBJECT_CREATE
			}
			ServerAPI.iam = DATA_PLAYER_PLAYER1;
		}
		ServerAPI.websocket.send(JSON.stringify(event));
	});
}

ServerAPI._Recv = function() {
	ServerAPI.websocket.addEventListener("message", ({data}) => {
		const event = JSON.parse(data);

		if (event[METHOD] != FROM_SERVER)
			return ;

		switch (event[OBJECT]) {
			case OBJECT_PADDLE:
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
	if (event[DATA_PLAYER] === DATA_PLAYER_PLAYER1 && ServerAPI.iam === DATA_PLAYER_PLAYER1) {
		ServerAPI.self_pos_promise = ServerAPI.self_pos_promise.then(async () => {
			ServerAPI.self_pos = new Vec2(event[DATA_POSITION][0], event[DATA_POSITION][1])});
		ServerAPI.self_key_promise = ServerAPI.self_key_promise.then(async () => {
			ServerAPI.self_key = event[DATA_INPUT]});
		ServerAPI.self_new_data = true;
	}
	if (event[DATA_PLAYER] === DATA_PLAYER_PLAYER1 && ServerAPI.iam !== DATA_PLAYER_PLAYER1) {
		ServerAPI.opp_pos_promise = ServerAPI.opp_pos_promise.then(async () => {
				ServerAPI.opp_pos = new Vec2(event[DATA_POSITION][0], event[DATA_POSITION][1])});
		ServerAPI.opp_key_promise = ServerAPI.opp_key_promise.then(async () => {
			ServerAPI.opp_key = event[DATA_INPUT]});
		ServerAPI.opp_new_data = true;
	}
	if (event[DATA_PLAYER] === DATA_PLAYER_PLAYER2 && ServerAPI.iam === DATA_PLAYER_PLAYER2) {
		ServerAPI.self_pos_promise = ServerAPI.self_pos_promise.then(async () => {
			ServerAPI.self_pos = new Vec2(event[DATA_POSITION][0], event[DATA_POSITION][1])});
		ServerAPI.self_key_promise = ServerAPI.self_key_promise.then(async () => {
			ServerAPI.self_key = event[DATA_INPUT]});
		ServerAPI.self_new_data = true;
	}
	if (event[DATA_PLAYER] === DATA_PLAYER_PLAYER2 && ServerAPI.iam !== DATA_PLAYER_PLAYER2) {
		ServerAPI.opp_pos_promise = ServerAPI.opp_pos_promise.then(async () => {
				ServerAPI.opp_pos = new Vec2(event[DATA_POSITION][0], event[DATA_POSITION][1])});
		ServerAPI.opp_key_promise = ServerAPI.opp_key_promise.then(async () => {
			ServerAPI.opp_key = event[DATA_INPUT]});
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
	// assert(key === DATA_INPUT_KEY_UP || key === DATA_INPUT_KEY_DOWN)

	const event = {
		[METHOD]: FROM_CLIENT,
		[OBJECT]: OBJECT_PADDLE,
		[DATA_INPUT]: key
	}
	ServerAPI.websocket.send(JSON.stringify(event));
}

export default ServerAPI;
