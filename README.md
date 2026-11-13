**Lancer l'application depuis interface.py**

**Points d'attentions et bugs connus** 

Il y a des bugs non bloquant pour un MVP qui existent et dont je n'ai pas eu le temps de corriger ainsi que certains choix voulu.

- Quitter l'application ne ferme pas le serveur lancé. Il faut interrompre dans la console
- Le texte du label ne se mets pas à jour, à la place il y a un print qui indique la prédiction s'il va pleuvoir ou non dans l'heure
- Le site des données n'autorise que de télécharger une semaine de donnée par API.
- Le site donnant les données par heure j'ai jugé OK pour un MVP de créer un modèle qui prédisait pour l'heure suivante.
- Le site des données demandant un compte et regardant l'adresse ip pour le token, il est possible que l'utilisateur suivant doivent se créer son propre token. 
  Le token actuel se trouve dans .env Il y a déjà une base de données de prête si le changement d'adresse ip est bloquant.

- Pour un hébergement plus responsable