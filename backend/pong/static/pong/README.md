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
  - [feature] Lobby time limit (5 minutes)
  - [refactor] Waiting room method

- View
  - Wrong username error

- Client
  - UI - lobby info 
  - [feature] tournament round info
  - [bug] ui not really showing at connection
  - [bug] score+names missing at reconnection

### Tournament
- [view] create && add
  - only authorized
  - only 'looking_for_players'

#### General
- WSS

### Maybe
- Stacking toasters