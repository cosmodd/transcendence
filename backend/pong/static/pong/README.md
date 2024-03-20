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
  - Ready State (for pre-created rooms)
    - Ready bool
    - Ready button
  - GameModel foreign key with UserModel
  - GameModel.asave() (username?-> fetched with token)
  - GameModel views
  - [bug?] paddle reset inconsistent
  - [bug?] pause time inconsistent

  - Create room duel
  - Tournament
  - Refactor

- Client
  - UI - print username
  - [bug] Local score 0 - 1

#### General
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
