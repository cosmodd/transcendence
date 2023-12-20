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

let opponentPosPromise = Promise.resolve();
let opponentPos = new Vec2(0., 0.);

// Namespace equivalent
let WebsocketLogic = {};

window.addEventListener("DOMContentLoaded", () => {
	WebsocketLogic.websocket = new WebSocket("ws://localhost:8888");

	// Events
	WebsocketLogic._initGame();
	WebsocketLogic._recv()
});

WebsocketLogic._initGame = function() {
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

WebsocketLogic._recv = function() {
	WebsocketLogic.websocket.addEventListener("message", ({data}) => {
		const event = JSON.parse(data);
		switch (event.type) {
			case "get":
				opponentPosPromise = opponentPosPromise.then(async () => {
					opponentPos = new Vec2(event.position[0], event.position[1]);
				});
				break;
			default:
				// throw new Error(`Unsupported event type: ${event.type}.`);
				console.log(event);
		}
	});
}

WebsocketLogic.getDataPaddle = async function() {
	await opponentPosPromise;
	return opponentPos.clone();
}

WebsocketLogic.sendDataPaddle = function(position) {
	position.x *= -1.;
	let event = {
		type: "send",
		object: "paddle",
		position: position.toArray()
	}
	WebsocketLogic.websocket.send(JSON.stringify(event));
}

export default WebsocketLogic;
