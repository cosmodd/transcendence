//  Game logic events
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
// * Type
//	- Join
//		- Create room or got a token ?
window.addEventListener("DOMContentLoaded", () => {
	const websocket = new WebSocket("ws://localhost:8888");

	// // Events
	// _initGame();
});

// Namespace equivalent
let websocketLogic = {};

// websocketLogic._initGame = function() {
//     const params = new URLSearchParams(window.location.search);
//     let event = { type: "join" };
//     if (params.has("join")) {
//       event.join = params.get("join");
//     } 
//     websocket.send(JSON.stringify(event));
// }
