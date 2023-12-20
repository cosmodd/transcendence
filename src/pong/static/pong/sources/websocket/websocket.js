//  Game logic events
//	* Type => game
//	* Method
//		- Get
//		- Send
//	* Object
//		- Ball
//		- Paddle
//	* Data
//		- Position
//		- Speed [Ball?]
//		- Acceleration [Ball]

// General events // Temporaire
// * Type => init
// * Join

import { Vec2 } from '../utils/class_vec.js';

let opp_pos_promise = Promise.resolve();
let opp_pos = new Vec2(0., 0.);

// Namespace equivalent
let WebsocketLogic = {};

window.addEventListener("DOMContentLoaded", () => {
	WebsocketLogic.websocket = new WebSocket("ws://localhost:8888");

	// Events
	WebsocketLogic._InitGame();
	WebsocketLogic._Recv()
});

WebsocketLogic._InitGame = function() {
	WebsocketLogic.websocket.addEventListener("open", () => {
		const params = new URLSearchParams(window.location.search);
		let event = { type: "init" };

		// Joining 
		if (params.has("join")) {
			event.join = params.get("join");
			WebsocketLogic.websocket.send(JSON.stringify(event));
		} 
		// Creating
		else {
		}

		WebsocketLogic.websocket.send(JSON.stringify(event));
	});
}

WebsocketLogic._Recv = function() {
	WebsocketLogic.websocket.addEventListener("message", ({data}) => {
		const event = JSON.parse(data);
		switch (event.type) {
			case "get":
				opp_pos_promise = opp_pos_promise.then(async () => {
					opp_pos = new Vec2(event.position[0], event.position[1]);
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
		type: "send",
		object: "paddle",
		position: position.ToArray()
	}
	WebsocketLogic.websocket.send(JSON.stringify(event));
}

export default WebsocketLogic;
