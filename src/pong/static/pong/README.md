## Server authority
Le serveur:
- Recoit: les nouveaux inputs (si changement avec frame precedente)
- Calcul mouvements et collisions
- Envoie: (a tous) nouvel input, nouvelle position
  
Les clients:
- Envoie: un nouvel input (p.ex. KeyUp->KeyNone)
- Recoit: nouvelles positions, nouveaux inputs (si changement avec frame precedente)
- Interpolation locale des positions (si aucun changement d'input avec frame precedente)

## Todo
#### General
* 2 players via Websockets
* 2 players via local/ia
* UX 

#### Websocket
- server.py 
	- receive currentscale at room creation ?
	- Refactor - constants Object_create in Data_info

- Websocket.js 
	- interpolation seulement si pas de data ?
	- Send & receive errors (shutdown server ingame to test)

#### General
- Score
- BallPaddle - ball.direction.y selon endroit de la collision ?
- Ball Reset - selon le gagnant
- Collision - meilleur collision paddle/ball
- Reconnexion

#### Guidelines
- ES.22
- NL.17
