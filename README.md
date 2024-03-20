# Suika agent


- game_results: contient les résultats de chaque partie.

- agent_cleaning.py: permet de nettoyer les sauvegardes temporaires des modèles des agents qui sont faites toutes les 5 parties, et de ne conserver que la dernière.

- charts.py: Graphiques présents sur le poster.

- config.py: Class config pour le jeu.

- config.yaml: Informations de configurations pour le jeu.

- game_classes.py: objects et fonctions utiles pour le jeux, et pour récupéré l'état du jeu à transmettre à l'agent.

- dqn_discrete_agent.py: Class DQNAgent.

- dqn_model.py: Model utilisé par les DQNAgents.

- play_dqn_discrete_game.py: Permet de créer un instance de jeu dans laquelle un DQNAgent va pouvoir jouer une ou plusieurs parties.

- play_game.py: Permet de créer un instance de jeu pour jouer vous même.

- play_random_game.py: Permet de créer un instance de jeu dans laquelle les coups sont joués aléatoirement.

- play_with_recovered_agent.py: Permet de créer un instance de jeu dans laquelle on fait jouer un model préalablement enregistré.

- make_trained_agent_play.py: Permet de faire rejouer les modèles enregistrés par les agents sans phase d'entrainement.

- multiple_games.py: Permet de lancer simultanément plusieurs parties.

Les fichier relatifs à l'implémentations du jeux sont des version adaptés de https://github.com/Ole-Batting/suika
Merci à Ole-Batting pour son travail.
