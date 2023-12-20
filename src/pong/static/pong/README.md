## Todo
#### General
* 2 players via Websockets
* 2 players via local/ia
* UX 

#### Websocket
- spectator logic !
- server.py - Server authority
	- send constants to game state
	- assert new_position is within rules
	- send position.x * -1
- server.py - Logic optimization
	- asyncio.lock() ?
- Websocket.js - Logic optimization
	- change event.method by event.METHOD

#### Specific
- Collision - ball reste dans les murs?
- Collision - meilleur collision paddle/ball
- UpdatePosition in shader ?

#### Guidelines
- ES.22
- NL.17
