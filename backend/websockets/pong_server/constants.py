__all__ = [
	"METHOD",
	"FROM_SERVER",
	"FROM_CLIENT",
	
	"OBJECT",
	"OBJECT_BALL",
	"OBJECT_PADDLE",
	"OBJECT_LOBBY",
	"OBJECT_INFO",

	"DATA_TIME",
	"DATA_LOBBY_STATE",
	"DATA_LOBBY_CREATE",
	"DATA_LOBBY_JOIN",
	"DATA_LOBBY_SEARCH",
	"DATA_LOBBY_ROOM_CREATED",
	"DATA_LOBBY_ROOM_ENDED",
	"DATA_LOBBY_ROOM_PAUSED",
	"DATA_LOBBY_ROOM_RECONNECTED",
	"DATA_LOBBY_ROOM_ID",
	"DATA_LOBBY_JOINKEY",
	"DATA_LOBBY_SCORE",
	"DATA_PLAYER_TOKEN",
	"DATA_POSITION",
	"DATA_DIRECTION",
	"DATA_ACCELERATION",
	"DATA_INPUT",
	"DATA_INPUT_KEY_UP",
	"DATA_INPUT_KEY_DOWN",
	"DATA_INPUT_KEY_NONE",
	"DATA_PLAYER",
	"DATA_PLAYER_PLAYER1",
	"DATA_PLAYER_PLAYER2",

	"DATA_INFO_TYPE",
	"DATA_INFO_TYPE_ERROR",
	"DATA_INFO_TYPE_MESSAGE",

	"kBallSpeed",
	"kBallAccelerationStep",
	"kBallRadius",
	"kPaddleSpeed",
	"kPaddleWidth",
	"kPaddleHeight",	
	"kScalingFactor",
	"kScoreLimit",
	"kGameDuration",
	"kReconnectionWaitingTime"
	]

METHOD = "Method"
FROM_SERVER = "FromServer"
FROM_CLIENT = "FromClient"

OBJECT = "Object"
OBJECT_BALL = "Ball"
OBJECT_PADDLE = "Paddle"
OBJECT_LOBBY = "Lobby"
OBJECT_INFO = "Info"
DATA_TIME = "Time"
DATA_INPUT = "Input"
DATA_INPUT_KEY_UP = "KeyUp"
DATA_INPUT_KEY_DOWN = "KeyDown"
DATA_INPUT_KEY_NONE = "None"
DATA_PLAYER = "Player"
DATA_PLAYER_PLAYER1 = "p1"
DATA_PLAYER_PLAYER2 = "p2"
DATA_LOBBY_STATE = "State"
DATA_LOBBY_CREATE = "Create"
DATA_LOBBY_JOIN = "Join"
DATA_LOBBY_SEARCH = "Search"
DATA_LOBBY_ROOM_CREATED = "Room_Created"
DATA_LOBBY_ROOM_ENDED = "Room_Ended"
DATA_LOBBY_ROOM_PAUSED = "Room_Paused"
DATA_LOBBY_ROOM_RECONNECTED = "Room_Reconnected"
DATA_LOBBY_ROOM_ID = "Room_ID"
DATA_LOBBY_JOINKEY = "JoinKey"
DATA_LOBBY_SCORE = "Score"
DATA_PLAYER_TOKEN = "Token"
DATA_POSITION = "Position"
DATA_DIRECTION = "Direction"
DATA_ACCELERATION = "Acceleration"
DATA_INFO_TYPE = "Info_Type"
DATA_INFO_TYPE_ERROR = "Error"
DATA_INFO_TYPE_MESSAGE = "Message"


kBallSpeed = 1.0 
kBallAccelerationStep = 0.1 
kBallRadius = 0.02
kPaddleSpeed = 1.5
kPaddleWidth = 0.05
kPaddleHeight = 0.3
kScalingFactor = [1.0, 1.25] # temporary ?
kScoreLimit = 10
kGameDuration = 30
kReconnectionWaitingTime = 5