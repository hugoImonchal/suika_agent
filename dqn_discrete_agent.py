import numpy as np
import random
from collections import deque
from dqn_model import create_dqn_mixte_model
import numpy as np
import random
from collections import deque
import uuid


class DQNAgent:
    def __init__(self, state_shape, num_scalars, action_size, last_layer_activation):
        self.id = str(uuid.uuid4())
        self.state_shape = state_shape  # (width, height, channels) pour l'image
        self.num_scalars = num_scalars  # Nombre de valeurs scalaires
        self.action_size = action_size  # Taille de l'espace d'action
        self.memory = deque(maxlen=1000)  # Mémoire de replay
        self.gamma = 0.95  # facteur de discount
        self.epsilon = 1.0  # exploration initiale
        self.epsilon_min = 0.01 # esploration minimale
        self.epsilon_decay = 0.995 # facteur de décroissance d'exploration
        self.nb_training = 0
        self.forget_after_training_probability = 0.2 
        self.model = create_dqn_mixte_model(self.state_shape, self.num_scalars, action_space=action_size, action_space_activation=last_layer_activation)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state, explore = True):
        if np.random.rand() <= self.epsilon and explore:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
    def replay(self, batch_size):
        self.nb_training += 1
        minibatch_indices = random.sample(range(len(self.memory)), min(len(self.memory), batch_size))
        minibatch = [self.memory[i] for i in minibatch_indices]
        n = 1
        for state, action, reward, next_state, done in minibatch:
                target = reward
                if not done:
                    target = (reward + self.gamma * np.amax(self.model.predict(next_state)[0]))
                target_f = self.model.predict(state)
                target_f[0][action] = target
                self.model.fit(state, target_f, epochs=1, verbose=0)
        for i in sorted(minibatch_indices, reverse=True):
            if random.random() > self.forget_after_training_probability:
                del self.memory[i]
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
# Usage
#agent = DQNAgent(state_shape=(64, 64, 1), num_scalars=2, action_size=3, last_layer_activation='linear')
