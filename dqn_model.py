import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, Flatten, Dense, Concatenate
from tensorflow.keras.optimizers import Adam

def create_dqn_model(input_shape, action_space=1, action_space_activation='linear'):
    """
    Crée un modèle DQN avec une architecture CNN.

    :param input_shape: La forme de l'état d'entrée (par exemple, une image du jeu).
    :param action_space: Le nombre d'actions possibles que l'agent peut prendre. (1)
    :param action_space_activation: Fonction d'activation de la couche de sortie. (sigmoid pour une valeure entre 0 et 1)

    :return: Un modèle Keras.
    """
    model = models.Sequential()
    model.add(layers.Input(shape=input_shape))
    model.add(layers.Conv2D(32, (8, 8), strides=(4, 4), activation='relu'))
    model.add(layers.Conv2D(64, (4, 4), strides=(2, 2), activation='relu'))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.Flatten())
    model.add(layers.Dense(512, activation='relu'))
    model.add(layers.Dense(action_space, activation=action_space_activation))  # Pas d'activation softmax car ce sont des valeurs Q.

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.00025),
                  loss='mse')  # mse pour la regression des valeurs Q.
    return model


def create_dqn_mixte_model(image_shape, num_scalars, action_space=1, action_space_activation='sigmoid'):
    """
    Crée un modèle DQN mixte pour traiter à la fois des images et des données scalaires.

    :param image_shape: dimensions de l'image
    :param num_scalars: Le nombre de valeurs scalaires à traiter (par exemple, 2 pour les rayons des fruits).
    :param action_size: Le nombre d'actions possibles (taille de l'espace d'action).
    :return: Un modèle TensorFlow/Keras.
    """
    
    # Branche CNN pour l'image du plateau de jeu
    input_image = Input(shape=image_shape, name='input_image')
    x = Conv2D(32, kernel_size=(3, 3), activation='relu')(input_image)
    x = Conv2D(64, (3, 3), activation='relu')(x)
    x = Flatten()(x)
    
    # Branche Dense pour les scalaires (rayons des fruits)
    input_scalars = Input(shape=(num_scalars,), name='input_scalars')
    y = Dense(32, activation='relu')(input_scalars)
    
    # Fusion des branches
    combined = Concatenate()([x, y])
    
    # Couches finales après la fusion
    z = Dense(64, activation='relu')(combined)
    z = Dense(32, activation='relu')(z)
    output = Dense(action_space, activation=action_space_activation, name='output')(z)  # Ajustez selon votre espace d'action
    
    # Création du modèle complet
    model = Model(inputs=[input_image, input_scalars], outputs=output)
    
    # Compilation du modèle
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
    
    return model

# create_dqn_model((128, 128, 1), action_space=1, action_space_activation='sigmoid')
create_dqn_mixte_model((128, 128, 1), 2, action_space=1, action_space_activation='sigmoid')
