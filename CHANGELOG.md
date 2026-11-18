# Historique des versions

## Tableau de bord (`index.html`)
- **v1.0** : état de préparation en direct (cerveau, voix, partie en cours), schéma du fonctionnement, étapes pour jouer, pièces du projet, décisions, aide et lexique.

## App de jeu (`jouer.html`)
- **v2.0** : bouton ⌂ vers le tableau de bord ; les réglages s'ouvrent directement depuis le tableau de bord.
- **v1.9** : VoiceStudio utilise une voix standard par défaut si aucune voix n'est choisie ; les voix personnelles s'ajoutent à la liste.
- **v1.8** : VoiceStudio passe par le serveur local du Mac (`serveur-mj.py`), sur le Mac comme sur le téléphone.
- **v1.7** : nouveau moteur de voix VoiceStudio, avec casting par personnage.
- **v1.6** : erreurs ElevenLabs et OpenAI expliquées, un seul message en cas de clé refusée.
- **v1.5** : lecture audio fiable sur iPhone (mode silencieux, retour depuis une autre app), répliques demandées une par une.
- **v1.4** : choix des voix ElevenLabs par personnage dans les réglages.
- **v1.3** : accepte les réponses copiées depuis un bloc de code.
- **v1.2** : mode copier-coller gratuit (Projet Claude).
- **v1.1** : mode API moins cher (cache de l'historique).
- **v1.0** : avatar, voix, dictée, sauvegarde de la partie.

## Banc d'essai des voix (`banc.html`)
- **v1.3** : lecture audio fiable sur iPhone.
- **v1.2** : lien vers l'app de jeu.
- **v1.1** : voix Piper (gratuites, hors ligne).
- **v1.0** : voix OpenAI et ElevenLabs, effets VHS.

## Serveur local (`serveur-mj.py`)
- **v1.0** : sert l'app depuis le Mac et relaie les voix vers VoiceStudio.
