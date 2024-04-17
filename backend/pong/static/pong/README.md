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
  - Create room duel
  - Tournament

- View
  - Wrong username error

- Client
  - UI - lobby info 
  - [bug] local score 0 - 1
  - [bug?] Score/Time not loading

#### General
- WSS

### Maybe
- Stacking toasters

#### Guidelines
- ES.22
- NL.17
