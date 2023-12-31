import { NewPaddleState, NewBallState } from './objects_state.js'

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

ServerAPI.GetBallState = async function()
{
	await ServerAPI.ball_state.promise;
	return { ...ServerAPI.ball_state };
}

ServerAPI.GetOpponentState = async function()
{
	await ServerAPI.opponent_state.promise;
	ServerAPI.opponent_state.new_data_available = false;
	return { ...ServerAPI.opponent_state};
}

ServerAPI.GetPlayerState = async function()
{
	await ServerAPI.player_state.promise;
	ServerAPI.player_state.new_data_available = false;
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
