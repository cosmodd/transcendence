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
  
Channels
  - [feature][->] warn users expected for next game
  - [feature][<-] receive NewRoom orders 

- Client
  - [bug] ui not loading #anger

#### General
- WSS

### Maybe
- Stacking toasters