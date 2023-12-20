## Todo
#### General
* 2 players via Websockets
* 2 players via local/ia
* UX 

#### Websocket
- server.py - Server authority
	- send constants to game state
	- assert new_position is within rules
- server.py - Logic optimization
	- asyncio.lock() ?
- Websocket.js - Logic optimization
	- change name of "get" and "send" types
- Websocket.js - refactor methods

#### Specific
- Collision - ball reste dans les murs?
- Collision - meilleur collision paddle/ball
- UpdatePosition in shader ?

#### Guidelines
- ES.22
- NL.17
