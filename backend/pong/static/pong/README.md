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
  - token dictionary for finding games
  - GameModel foreign key with UserModel
  - GameModel.asave() (username?-> fetched with token)
  - GameModel views
  - [error] already registered in a room
  - [bug] paddle reset inconsistent
  - [bug] pause time inconsistent ?

  - Create room duel
  - Tournament
  - Refactor

- Client
  - UI - print username
  - [bug] Local score 0 - 1

#### General
- UI et UX
- Casual
- Tournaments
- Invitations (Duel)

### Maybe
- Customization (minor)
- Lobby constantes modifiables (score, time limit, etc)

#### Guidelines
- ES.22
- NL.17
