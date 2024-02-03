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
- Server
	- receive currentscale at room creation ?

- Client
  - IA + API
  - Redondance GameType / DataOrigin ?

#### General
- Ball Reset - selon le gagnant + attente
- Collision - meilleur collision paddle/ball
  - ball.direction.y selon endroit de la collision ?
  - top et bottom collision
- Reconnexion
- Server optimisation
- Local coop ?

#### Guidelines
- ES.22
- NL.17
