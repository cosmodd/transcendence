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
- SSL
  - un seul certificat

- Server
  - [feature] Lobby time limit (5 minutes)
  
Channels
  - [feature][->] warn users expected for next game
  - [feature][<-] receive NewRoom orders 
    - to secure

- Client
  - [bug] ui not loading #anger

#### General
- Rename websockets folder
- Clean