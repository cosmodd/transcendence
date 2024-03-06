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
- Reconnexion
  - Pause time inconsistent

- Server
  - Reco handler -> game method
  - Refactor gamelogic - reconnexion
  - Add room created to MessageBuilder
  - Create room duel
  - Refactor

- Client
  - index.html import 
  - Refactor server_handler

#### General
- Collision - bugs
- UI et UX
- Lobby constantes modifiables (score, time limit, etc)
- Casual
- Tournaments
- Invitations
- Front Integration
- Back Integration

### Maybe
- Customization (minor)

#### Guidelines
- ES.22
- NL.17
