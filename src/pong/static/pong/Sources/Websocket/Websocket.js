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

window.addEventListener("DOMContentLoaded", () => {
	const websocket = new WebSocket("ws://localhost:8888");

	// // Events
	websocketLogic._initGame(websocket);
});

// Namespace equivalent
let websocketLogic = {};

websocketLogic._initGame = function(websocket) {
	websocket.addEventListener("open", () => {
		const params = new URLSearchParams(window.location.search);
		let event = { type: "init" };

		// Joining 
		if (params.has("join")) {
			event.join = params.get("join");
			websocket.send(JSON.stringify(event));
		} 
		// Creating
		else {
		}

		websocket.send(JSON.stringify(event));

		websocket.addEventListener("message", (event) => {
			console.log(event.data);
		});
	});
}
