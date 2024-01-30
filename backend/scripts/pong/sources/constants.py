__all__ = [
	"METHOD",
	"FROM_SERVER",
	"FROM_CLIENT",
	
	"OBJECT",
	"OBJECT_BALL",
	"OBJECT_PADDLE",
	"OBJECT_LOBBY",
	"OBJECT_INFO",

	"DATA_LOBBY_STATE",
	"DATA_LOBBY_CREATE",
	"DATA_LOBBY_JOIN",
	"DATA_LOBBY_JOINKEY",
	"DATA_LOBBY_SCORE",
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
	"kScalingFactor"	
	]

METHOD = "Method"
FROM_SERVER = "FromServer"
FROM_CLIENT = "FromClient"

OBJECT = "Object"
OBJECT_BALL = "Ball"
OBJECT_PADDLE = "Paddle"
OBJECT_LOBBY = "Lobby"
OBJECT_INFO = "Info"
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
DATA_LOBBY_JOINKEY = "JoinKey"
DATA_LOBBY_SCORE = "Score"
DATA_POSITION = "Position"
DATA_DIRECTION = "Direction"
DATA_ACCELERATION = "Acceleration"
DATA_INFO_TYPE = "Info_Type"
DATA_INFO_TYPE_ERROR = "Error"
DATA_INFO_TYPE_MESSAGE = "Message"


kBallSpeed = 0.5
kBallAccelerationStep = 0.1 
kBallRadius = 0.02
kPaddleSpeed = 2.0
kPaddleWidth = 0.05
kPaddleHeight = 0.2
kScalingFactor = [1.0, 1.25] # temporary