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
  - Tournament logic
  - [error] signed in a tournament 

- View
  - Wrong username error

- Models
  - Tournament

- Client
  - UI - lobby info 
  - [bug] score missing at reconnection

### Tournament
- [view] create && add
  - only authorized

- Logique
  - 1ere etape 
   - Crees a la premiere connexion
  - Autres etapes
   - Crees au dernier match d’un bracket

#### General
- WSS

### Maybe
- Stacking toasters