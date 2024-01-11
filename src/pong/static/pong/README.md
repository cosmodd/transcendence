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

#### Specific
- server.py 
	- receive currentscale at room creation ?

- Websocket.js 
	- Game Class and instance

#### General
- Score
- Ball Reset - selon le gagnant + attente
- Collision - meilleur collision paddle/ball
  - ball.direction.y selon endroit de la collision ?
- Reconnexion
- IA! / Local?

#### Guidelines
- ES.22
- NL.17
