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
  - Game types to GameModel (duel, tournament, casual)
  - [bug] ball reset inconsistent
  - [bug?] ready-lobby well implemented ?
  - [bug?] paddle reset inconsistent
  - [bug?] pause time inconsistent

  - Create room duel
  - Tournament
  - Refactor

- Client
  - Local - not working
  - UI - print username
  - UI - lobby infos (gametype, who is ready)
  - Remove room-uuid cookie
  - [bug] Local score 0 - 1
  - [bug?] Score/Time not loading (sometimes)

#### General
- WSS
- Tournaments
- Invitations (Duel)
- Local Game in Database ?
- Stacking toasters
- Casual Elo ?

### Maybe
- Customization (minor)
- Lobby constantes modifiables (score, time limit, etc)

#### Guidelines
- ES.22
- NL.17
