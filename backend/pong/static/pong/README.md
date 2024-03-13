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
  - UUID replaced by Username
  - Create room duel
  - Tournament
  - Refactor
  - Pause time inconsistent ?

- Client
 - Local score 0 - 1 bug

#### General
- Collision - bugs
- UI et UX
- Casual
- Tournaments
- Invitations (Duel)
- Front Integration
- Back Integration

### Maybe
- Customization (minor)
- Lobby constantes modifiables (score, time limit, etc)

#### Guidelines
- ES.22
- NL.17
