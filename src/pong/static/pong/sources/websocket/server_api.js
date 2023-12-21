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
const DATA_JOINKEY = "JoinKey"; // - Join key
const DATA_POSITION = "Position"; // - Data position

import { Vec2 } from '../utils/class_vec.js';


// Namespace equivalent
let ServerAPI = {};

ServerAPI.opp_pos_promise = Promise.resolve();
ServerAPI.opp_pos = new Vec2(2., 2.); // Out of bounds


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
		} 
		// Creating
		else {
			event = {	[METHOD]: FROM_CLIENT,
						[OBJECT]: OBJECT_CREATE
			}
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
				ServerAPI.opp_pos_promise = ServerAPI.opp_pos_promise.then(async () => {
					ServerAPI.opp_pos = new Vec2(event[DATA_POSITION][0], event[DATA_POSITION][1]);
				});
				break;
			default:
				// throw new Error(`Unsupported event type: ${event.type}.`);
				console.log(event);
		}
	});
}

ServerAPI.GetDataPaddle = async function() {
	await ServerAPI.opp_pos_promise;
	return ServerAPI.opp_pos.Clone();
}

ServerAPI.SendDataPaddle = function(position) {
	position.x *= -1.;
	let event = {
		[METHOD]: FROM_CLIENT,
		[OBJECT]: OBJECT_PADDLE,
		[DATA_POSITION]: position.ToArray()
	}
	ServerAPI.websocket.send(JSON.stringify(event));
}

export default ServerAPI;
