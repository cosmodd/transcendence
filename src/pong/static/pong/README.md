## Server authority
Le serveur:
- Recoit: les nouveaux inputs (si changement avec frame precedente)
- Calcul mouvements et collisions
- Envoie: (a tous) nouvel input, nouvelle position
  
Les clients:
- Envoie: un nouvel input (p.ex. KeyUp->KeyNone)
- Recoit: nouvelles positions, nouveaux inputs (si changement avec frame precedente)
- Interpolation locale des positions (si aucun changement avec frame precedente)

## Todo
#### General
* 2 players via Websockets
* 2 players via local/ia
* UX 

#### Websocket
- server.py - Server authority
	- Refactor - rename class_pong
	- Collision - send currentscale constant

- server.py - Logic optimization
	- asyncio.lock() ?
	- Vec2

- Websocket.js - Logic optimization and refactor
	- PlayerState global getter
	- new_data_available data race
	- check client collision only if interpolate

#### Client
- Collision - ball reste dans les murs?
- Collision - meilleur collision paddle/ball
- UpdatePosition in shader ?

#### Guidelines
- ES.22
- NL.17
