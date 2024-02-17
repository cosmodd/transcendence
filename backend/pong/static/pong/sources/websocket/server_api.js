import { NewPaddleState, NewBallState, NewScoreState } from './objects_state.js'

// Namespace equivalent
let ServerAPI = {};

// Server messaging logic
ServerAPI.METHOD = "Method";
/**/ServerAPI.FROM_SERVER = "FromServer"; // - FromServer
/**/ServerAPI.FROM_CLIENT = "FromClient"; // - FromClient
ServerAPI.OBJECT = "Object";
/**/ServerAPI.OBJECT_BALL = "Ball"; // - Ball
/**/ServerAPI.OBJECT_PADDLE = "Paddle"; // - Paddle
/**/ServerAPI.OBJECT_LOBBY = "Lobby";
/**/ServerAPI.OBJECT_INFO = "Info";
ServerAPI.DATA_INPUT = "Input";
/**/ServerAPI.DATA_INPUT_KEY_UP = "KeyUp";
/**/ServerAPI.DATA_INPUT_KEY_DOWN = "KeyDown";
/**/ServerAPI.DATA_INPUT_KEY_NONE = "None";
ServerAPI.DATA_PLAYER = "Player";
/**/ServerAPI.DATA_PLAYER_PLAYER1 = "p1";
/**/ServerAPI.DATA_PLAYER_PLAYER2 = "p2";
ServerAPI.DATA_LOBBY_STATE = "State";
/**/ServerAPI.DATA_LOBBY_CREATE = "Create";
/**/ServerAPI.DATA_LOBBY_JOIN = "Join";
/**/ServerAPI.DATA_LOBBY_SEARCH = "Search";
/**/ServerAPI.DATA_LOBBY_ROOM_CREATED = "Room_Created";
/**/ServerAPI.DATA_LOBBY_ROOM_ENDED = "Room_Ended";
/**/ServerAPI.DATA_LOBBY_ROOM_PAUSED = "Room_Paused";
ServerAPI.DATA_LOBBY_ROOM_ID = "Room_ID";
ServerAPI.DATA_LOBBY_JOINKEY = "JoinKey"; // - Join key
ServerAPI.DATA_LOBBY_SCORE = "Score"; // - Join key
ServerAPI.DATA_PLAYER_UUID = "UUID";
ServerAPI.DATA_INFO_TYPE = "Info_Type";
/**/ServerAPI.DATA_INFO_TYPE_ERROR = "Error";
/**/ServerAPI.DATA_INFO_TYPE_MESSAGE = "Message";
ServerAPI.DATA_POSITION = "Position";
ServerAPI.DATA_DIRECTION = "Direction";
ServerAPI.DATA_ACCELERATION = "Acceleration";

// Constants

// Objects state initialization
ServerAPI.player_state = null;
ServerAPI.opponent_state = null;
ServerAPI.ball_state = NewBallState();
ServerAPI.score_state = NewScoreState(); 
ServerAPI.iam = "";

ServerAPI.NewBallStateAvailable = async function()
{
	await ServerAPI.ball_state.promise;
	return (ServerAPI.ball_state.new_data_available);
}

ServerAPI.NewPlayerStateAvailable = async function()
{
	await ServerAPI.player_state.promise;
	return (ServerAPI.player_state.new_data_available);
}

ServerAPI.NewOpponentStateAvailable = async function()
{
	await ServerAPI.opponent_state.promise;
	return (ServerAPI.opponent_state.new_data_available);
}

ServerAPI.NewScoreStateAvailable = async function()
{
	await ServerAPI.score_state.promise;
	return (ServerAPI.score_state.new_data_available);
}

ServerAPI.GetBallState = async function()
{
	await ServerAPI.ball_state.promise;
	ServerAPI.ball_state.promise = ServerAPI.ball_state.promise.then(async () => {
		ServerAPI.ball_state.new_data_available = false;
	});
	return { ...ServerAPI.ball_state };
}

ServerAPI.GetOpponentState = async function()
{
	await ServerAPI.opponent_state.promise;
	ServerAPI.opponent_state.promise = ServerAPI.opponent_state.promise.then(async () => {
		ServerAPI.opponent_state.new_data_available = false;
	});
	return { ...ServerAPI.opponent_state};
}

ServerAPI.GetPlayerState = async function()
{
	await ServerAPI.player_state.promise;
	ServerAPI.player_state.promise = ServerAPI.player_state.promise.then(async () => {
		ServerAPI.player_state.new_data_available = false;
	});
	return { ...ServerAPI.player_state};
}

ServerAPI.GetScoreState = async function()
{
	await ServerAPI.score_state.promise;
	ServerAPI.score_state.promise = ServerAPI.score_state.promise.then(async () => {
		ServerAPI.score_state.new_data_available = false;
	});
	return { ...ServerAPI.score_state};
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
