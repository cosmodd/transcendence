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
- Game
  - [bug] ball stuck on one side
  - [bug] ready while disco -> added timer
  - [bug] bad ui (infos) placement
  - [check] tournament cancel game behavior ?

- Channels
  - [feature][->] warn users expected for next game

- Client
  - [bug] ui not loading #anger

#### General
- Clean