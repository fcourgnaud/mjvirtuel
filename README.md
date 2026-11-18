# MJ virtuel

Un meneur de jeu de rôle virtuel, « la Voix », qui fait jouer un scénario à des joueurs autour d'une table, avec une voix différente pour chaque personnage. Premier jeu : *Channel Fear* (Mister Frankenstein).

**Tester en ligne : https://fcourgnaud.github.io/mjvirtuel/**

| Page | Rôle |
|---|---|
| [`index.html`](https://fcourgnaud.github.io/mjvirtuel/) | Tableau de bord : où j'en suis, comment ça marche, comment jouer |
| [`jouer.html`](https://fcourgnaud.github.io/mjvirtuel/jouer.html) | L'app de jeu |
| [`banc.html`](https://fcourgnaud.github.io/mjvirtuel/banc.html) | Le banc d'essai des voix |
| `serveur-mj.py` | Serveur local du Mac, pour les voix VoiceStudio |

Historique des changements : [CHANGELOG.md](CHANGELOG.md).

## Ce qui n'est pas dans ce dépôt

Le dépôt est public. Les documents du meneur (brief de l'avatar, fiche système, fiche scénario, méthode) restent privés : le scénario vient d'un livre acheté. On les charge dans l'app (⚙ › Documents) ou dans un Projet Claude. Les clés API et les réglages sont gardés uniquement dans le navigateur de chaque appareil.

## Voix VoiceStudio (Mac)

1. Ouvrir VoiceStudio sur le Mac.
2. Télécharger `serveur-mj.py`, puis dans Terminal : `python3 ` + glisser le fichier + Entrée.
3. Ouvrir l'adresse affichée : `http://localhost:8000/jouer.html` sur le Mac, ou `http://ADRESSE-DU-MAC:8000/jouer.html` sur le téléphone (même wifi).

Le serveur sert les pages présentes dans le même dossier que lui : placer `jouer.html` et `banc.html` à côté de `serveur-mj.py`.

## Versions et mises à jour

- `version.json` contient les dernières versions publiées de chaque page.
- `maj.js` compare la version de la page ouverte à `version.json`. Si une version plus récente existe, un bandeau propose « Mettre à jour », qui recharge la page en contournant le cache.
- Pour publier une mise à jour : changer la version dans la page (`APP_VERSION` ou `MJV_PAGE`), la reporter dans `version.json` avec une note, et compléter `CHANGELOG.md`.
