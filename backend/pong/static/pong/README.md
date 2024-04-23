## Logic
Le serveur:
- Recoit: les nouveaux inputs (si changement avec frame precedente)
- Calcul mouvements et collisions
- Envoie: (a tous) nouvel input, nouvelle position
  
Les clients:
- Envoie: un nouvel input (p.ex. KeyUp->KeyNone)
- Recoit: nouvelles positions, nouveaux inputs (si changement avec frame precedente)
- Interpolation locale des positions (si aucun changement d'input avec frame precedente)

## Todo

#### Specific
- Server
  - Change token by username (+ encapsulate with try)
  - Change handler logic (accept multi type messages)
  - Create room duel
  - Tournament logic
  - [bug] both disconnected at same time (canceled game ?)

- View
  - Wrong username error

- Models
  - Tournament

- Client
  - UI - lobby info 
  - [bug] score missing at reconnection

#### General
- WSS

### Maybe
- Stacking toasters