import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Noms de colonnes 
col_names = ['agent_id', 'numero_partie', 'score_final', 'coups_joues']

### RANDOM GAMES 
df = pd.read_csv('./data/game_results/resultats_random_agents.csv', header=None, names=col_names)

scores_finaux = df['score_final']
moyenne = scores_finaux.mean()
ecart_type = scores_finaux.std()
variance = scores_finaux.var()

print(f"RANDOM AGENT - Moyenne des scores finaux : {moyenne}")
print(f"RANDOM AGENT - Écart-type des scores finaux : {ecart_type}")
print(f"RANDOM AGENT - Variance des scores finaux : {variance}")

# Création de l'histogramme des scores finaux
plt.figure(figsize=(10, 6))
plt.hist(scores_finaux, bins=20, color='skyblue', edgecolor='black')
plt.title('Histogramme des Scores Finaux (modèle aléatoire)')
plt.xlabel('Scores Finaux')
plt.ylabel('Nombre de parties')
plt.grid(axis='y', alpha=0.75)
plt.show()

# Création de la boîte à moustaches pour les scores finaux
plt.figure(figsize=(8, 6))
plt.boxplot(scores_finaux, vert=False, patch_artist=True, notch=True)
plt.title('Boîte à Moustaches des Scores Finaux')
plt.xlabel('Scores Finaux')
plt.show()


### DQN DISCRETE AGENT
df = pd.read_csv('./data/game_results/resultats_dqn_discrete_agents_2.csv', header=None, names=col_names)

scores_finaux = df['score_final']
moyenne = scores_finaux.mean()
ecart_type = scores_finaux.std()
variance = scores_finaux.var()

print(f"DQN AGENT - Moyenne des scores finaux : {moyenne}")
print(f"DQN AGENT - Écart-type des scores finaux : {ecart_type}")
print(f"DQN AGENT - Variance des scores finaux : {variance}")

plt.figure(figsize=(10, 6))  
sns.boxplot(x='numero_partie', y='score_final', data=df, color='lightgray')

# Ajouter les points de données
sns.stripplot(x='numero_partie', y='score_final', data=df, hue='agent_id', palette='tab10',  size=6, alpha=0.7, legend= False)

plt.title('Boîte à Moustaches des Scores Finaux en fonction de la partie jouée')
plt.xlabel('Numero de partie')
plt.ylabel('Score')

plt.show()

plt.figure(figsize=(12, 8))

# Utilisation de seaborn pour tracer la courbe de progression pour chaque agent
sns.lineplot(x='numero_partie', y='score_final', hue='agent_id', data=df, marker='o', palette='tab10', linewidth=2.5)

plt.title('Progression of Game Score by Agent')
plt.xlabel('Game Number')
plt.ylabel('Game Score')
plt.xticks(df['numero_partie'].unique()) 
plt.legend(title='Agent ID')

plt.grid(True)
plt.show()