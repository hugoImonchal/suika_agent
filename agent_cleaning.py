import os
import re

agents_folder = './data/agents'

latest_games = {}

# Trouver le fichier le plus récent pour chaque agent
for filename in os.listdir(agents_folder):
    match = re.match(r'dqn_discrete_(.*?)_after_game_([0-9]+)\.h5', filename)
    if match:
        agent_id = match.group(1)
        game_number = int(match.group(2))
        
        if agent_id not in latest_games or game_number > latest_games[agent_id][1]:
            latest_games[agent_id] = (filename, game_number)

# Supprimer ceux qui ne sont pas les plus récents
for filename in os.listdir(agents_folder):
    match = re.match(r'dqn_discrete_(.*?)_after_game_([0-9]+)\.h5', filename)
    if match:
        agent_id = match.group(1)
        game_number = int(match.group(2))
        latest_filename = latest_games[agent_id][0]      
        if filename != latest_filename:
            os.remove(os.path.join(agents_folder, filename))
            print(f"Supprimé : {filename}")

for agent_id, (filename, game_number) in latest_games.items():
    print(f"Conservé : Agent ID: {agent_id}, Latest Game Number: {game_number}, Filename: {filename}")