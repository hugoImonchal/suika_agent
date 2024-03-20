from multiprocessing import Process
from play_with_recovered_agent import recovered_agent_games
import os
import re
from collections import defaultdict
import pandas as pd

def lancer_parties_en_parallele():
    n_games = 30 # Nombre de parties par agents 
    n_agents = 15
    agents_dir = './data/agents'
    processus = []
    df_agents = pd.DataFrame(columns=['agent_id', 'games_played', 'path'])

    for filename in os.listdir(agents_dir):
        match = re.match(r'dqn_discrete_(.*?)_after_game_([0-9]+)\.h5', filename)
        if match:
            agent_id = match.group(1)
            game_number = int(match.group(2))
            file_path = agents_dir+ '/'+ filename
            df_agents = df_agents._append({'agent_id': agent_id, 'games_played': game_number, 'path': file_path}, ignore_index=True)

    df_agents_sorted = df_agents.sort_values(by='games_played', ascending=False)
    top_n_agents = df_agents_sorted.head(n_agents)


    for index, row in top_n_agents.iterrows():
        print(f"Agent ID: {row['agent_id']} - Games Played: {row['games_played']} - Path: {row['path']}")
        p = Process(target=recovered_agent_games, args=(row['agent_id'], row['agent_id'], row['path'], n_games))
        processus.append(p)
        p.start()

    for p in processus:
        p.join()


if __name__ == "__main__":
    lancer_parties_en_parallele()