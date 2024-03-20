from multiprocessing import Process
# from play_random_game import random_game
from play_dqn_discrete_game import dqn_discrete_games 

n_agent = 15 # Nombre d'agents à faire jouer en parrallele
n_games = 70 # Nombre de parties par agents 

def lancer_parties_en_parallele(number_of_agents, number_of_games):
    processus = []

    # Créer et démarrer les processus
    for i in range(number_of_agents):
        p = Process(target=dqn_discrete_games, args=(i,number_of_games))
        processus.append(p)
        p.start()

    # Attendre que tous les processus se terminent
    for p in processus:
        p.join()

if __name__ == "__main__":
    lancer_parties_en_parallele(n_agent, n_games)