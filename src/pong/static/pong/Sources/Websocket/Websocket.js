//  Game logic events
//	* Type => game
//	* Method
//		- Get
//		- Send
//	* Object
//		- Ball
//		- Player
//		- Opponent
//	* Data
//		- Position
//		- Speed [Ball?]
//		- Acceleration [Ball]

// General events // Temporaire
// * Type => init
// * Join

// Namespace equivalent
let WebsocketLogic = {};

window.addEventListener("DOMContentLoaded", () => {
	WebsocketLogic.websocket = new WebSocket("ws://localhost:8888");

	// Events
	WebsocketLogic._initGame();
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

		WebsocketLogic.websocket.addEventListener("message", (event) => {
			console.log(event.data);
		});
	});
}

WebsocketLogic.sendDataPaddle = function(position) {
	let event = {
		type: "send",
		object: "paddle",
		position: position.toArray()
	}
	WebsocketLogic.websocket.send(JSON.stringify(event));
}

export default WebsocketLogic;
