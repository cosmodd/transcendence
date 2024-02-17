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
* 2 players via local
* UX 

#### Specific
- Server
  - BUG - Finding room even if both players left earlier
  - ROOMS data race
  - Regrouper game.players et game.clients
  - Refactor

- Client
  - index.html import 
  - Reconnexion
    - Change "Searching for players..."
  - Refactor server_handler
#### General
- Collision - bugs
- Reconnexion
  - Systeme de pause
  - Message de reconnexion
- Score max constants
- Esthetique

#### Guidelines
- ES.22
- NL.17
