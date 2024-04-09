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
  - Change handler logic (accept chat server messages)
  - [bug] paddle badly placed (iam in reco ?)
  - [bug?] pause time inconsistent
  - Create room duel
  - Tournament

- View
  - Wrong username error

- Client
  - UI - usernames
  - UI - lobby infos (gametype, who is ready)
  - [bug] local score 0 - 1
  - [bug?] Score/Time not loading

#### General
- WSS

### Maybe
- Stacking toasters
- Customization (minor)
- Lobby constantes modifiables (score, time limit, etc)

#### Guidelines
- ES.22
- NL.17
