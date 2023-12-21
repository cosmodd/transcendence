## Todo
#### General
* 2 players via Websockets
* 2 players via local/ia
* UX 

#### Websocket
- server.py - Server authority
	- input based broadcast
	- asyncio.ensure_future(GameState())
	- send currentscale constant
	- Collision  - paddle with wall
- server.py - Logic optimization
	- asyncio.lock() ?
- Websocket.js - Logic optimization

#### Specific
- Collision - ball reste dans les murs?
- Collision - meilleur collision paddle/ball
- UpdatePosition in shader ?

#### Guidelines
- ES.22
- NL.17
