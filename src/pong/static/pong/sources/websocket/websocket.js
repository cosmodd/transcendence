//  Game logic events
const METHOD = "Method";
	const FROM_SERVER = "FromServer"; // - FromServer
	const FROM_CLIENT = "FromClient"; // - FromClient
const OBJECT = "Object";
	const OBJECT_BALL = "Ball"; // - Ball
	const OBJECT_PADDLE = "Paddle"; // - Paddle
	const OBJECT_JOIN = "Join"; // - Join
	const OBJECT_CREATE = "Create"; // - Create

//	* Data
//		- Position
//		- Speed [Ball?]
//		- Acceleration [Ball]
const DATA_JOINKEY = "JoinKey"; // - Join key

import { Vec2 } from '../utils/class_vec.js';

let opp_pos_promise = Promise.resolve();
let opp_pos = new Vec2(2., 2.); // Out of bounds

// Namespace equivalent
let WebsocketLogic = {};

window.addEventListener("DOMContentLoaded", () => {
	WebsocketLogic.websocket = new WebSocket("ws://localhost:8888");

	// Events
	WebsocketLogic._InitGame();
	WebsocketLogic._Recv()
});

WebsocketLogic._InitGame = function()
{
	WebsocketLogic.websocket.addEventListener("open", () => {
		const params = new URLSearchParams(window.location.search);
		let event = {}
		// Joining 
		if (params.has("join")) {
			event = {	Method: FROM_CLIENT,
						Object: OBJECT_JOIN,
						JoinKey: params.get("join")
			}
		} 
		// Creating
		else {
			event = {	Method: FROM_CLIENT,
						Object: OBJECT_CREATE
			}
		}
		WebsocketLogic.websocket.send(JSON.stringify(event));
	});
}

WebsocketLogic._Recv = function() {
	WebsocketLogic.websocket.addEventListener("message", ({data}) => {
		const event = JSON.parse(data);

		if (event.Method != FROM_SERVER)
			return ;

		switch (event.Object) {
			case OBJECT_PADDLE:
				opp_pos_promise = opp_pos_promise.then(async () => {
					opp_pos = new Vec2(event.Position[0], event.Position[1]);
				});
				break;
			default:
				// throw new Error(`Unsupported event type: ${event.type}.`);
				console.log(event);
		}
	});
}

WebsocketLogic.GetDataPaddle = async function() {
	await opp_pos_promise;
	return opp_pos.Clone();
}

WebsocketLogic.SendDataPaddle = function(position) {
	position.x *= -1.;
	let event = {
		Method: FROM_CLIENT,
		Object: OBJECT_PADDLE,
		Position: position.ToArray()
	}
	WebsocketLogic.websocket.send(JSON.stringify(event));
}

export default WebsocketLogic;
