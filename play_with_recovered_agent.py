from dqn_discrete_agent import DQNAgent
from game_classes import *
from config import Config
import sys
import pygame
import pymunk
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import mean_squared_error

def recovered_agent_games(id_instance, agent_id, agent_model_path, number_of_game=1):

    config = Config()
    board_width = config.playground_right - config.playground_left
    boarg_height = config.playground_bot - config.playground_top
    print(board_width, boarg_height)

    ### Init agent
    new_width = 76
    new_height = 100
    width_ratio = board_width/new_width
    model = tf.keras.models.load_model(agent_model_path,compile=False, custom_objects={'mse': tf.keras.metrics.MeanSquaredError()})
    model.summary()

    print(f"Agent {agent_id} initialisé")

    ### Init game 
    current_game = 1
    fps_interval = config.screen.fps*2
    print(f"Starting game {id_instance}, game {current_game}")
    
    # Create Pygame window
    screen = pygame.display.set_mode((config.screen.width, config.screen.height))
    pygame.display.set_caption("PySuika")
    clock = pygame.time.Clock()
    pygame.font.init()
    scorefont = pygame.font.SysFont("monospace", 32)
    overfont = pygame.font.SysFont("monospace", 72)

    space = pymunk.Space()
    space.gravity = (0, config.physics.gravity)
    space.damping = config.physics.damping
    space.collision_bias = config.physics.bias

    # Walls
    left = Wall(config.top_left, config.bot_left, space)
    bottom = Wall(config.bot_left, config.bot_right, space)
    right = Wall(config.bot_right, config.top_right, space)

    # List to store particles
    wait_for_next = 0
    cloud = Cloud()
    particles = []

    # Collision Handler
    handler = space.add_collision_handler(1, 1)

    handler.begin = collide
    handler.data["particles"] = particles
    handler.data["score"] = 0

    # Game vars
    game_over = False
    action_started = False
    initial_state = None
    moves = 0
    step_done = False
    previous_iter_score = 0
    last_fusion_frame = 9999
    frame_since_last_action = 0 

    while not game_over:
        
        if previous_iter_score > handler.data["score"]:
            last_fusion_frame = 0
        
        # Take user input
        if pygame.event.peek():
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    print(f"quit game {id_instance}")
                    pygame.quit()
                    sys.exit()
        
        # Agent action
        if (frame_since_last_action >= fps_interval) and (last_fusion_frame >= fps_interval) and  (action_started==False) and (wait_for_next == 0):
            action_started = True
            initial_score = handler.data["score"]
            initial_state = get_board_state_resized(particles, cloud, new_width, new_height)
            action = model.predict(initial_state)
            cloud.curr.set_x(action * width_ratio + config.playground_left)
            particles.append(cloud.release(space))
            step_done = False
            moves += 1
            frame_since_last_action = 0
            wait_for_next = config.screen.delay
            

        # Delay between fruit drop
        if wait_for_next > 1:
            wait_for_next -= 1
        if wait_for_next == 1:
            cloud.step()
            step_done = True
            wait_for_next -= 1

        # Draw background and particles
        screen.blit(config.background_blit, (0, 0))
        cloud.draw(screen, wait_for_next)
        for p in particles:
            p.draw(screen)
            if p.pos[1] < config.pad.killy and p.has_collided:
                label = overfont.render("Game Over!", 1, (0, 0, 0))
                screen.blit(label, (30, 160))
                game_over = True
        label = scorefont.render(f"Score: {handler.data['score']}", 1, (0, 0, 0))
        screen.blit(label, (10, 10))

        # Reward 
        if (frame_since_last_action >= fps_interval) and (last_fusion_frame >= fps_interval) and (action_started) and (wait_for_next == 0) and (step_done):
            action_started = False



        # Time step
        space.step(1/config.screen.fps)
        pygame.display.update()
        clock.tick(config.screen.fps)

        frame_since_last_action += 1
        last_fusion_frame += 1
        previous_iter_score = handler.data["score"]

        # Reset game if number_of_game > 1
        if (game_over == True and current_game < number_of_game ):
            print(f"End of instance {id_instance} game {current_game}, final score {handler.data['score']}")
            enregistrer_resultats('./data/game_results/resultats_recovered_dqn_discrete_agents.csv', agent_id, current_game, handler.data['score'], moves)
            
            current_game += 1
            print(f"Starting game {id_instance}, game {current_game}")

            screen = pygame.display.set_mode((config.screen.width, config.screen.height))
            pygame.display.set_caption("PySuika")
            clock = pygame.time.Clock()
            pygame.font.init()
            scorefont = pygame.font.SysFont("monospace", 32)
            overfont = pygame.font.SysFont("monospace", 72)
            space = pymunk.Space()
            space.gravity = (0, config.physics.gravity)
            space.damping = config.physics.damping
            space.collision_bias = config.physics.bias

            # Walls
            left = Wall(config.top_left, config.bot_left, space)
            bottom = Wall(config.bot_left, config.bot_right, space)
            right = Wall(config.bot_right, config.top_right, space)

            # List to store particles
            wait_for_next = 0
            cloud = Cloud()
            particles = []

            # Collision Handler
            handler = space.add_collision_handler(1, 1)
            handler.begin = collide
            handler.data["particles"] = particles
            handler.data["score"] = 0

            # Game vars
            game_over = False
            action_started = False
            initial_state = None
            moves = 0
            step_done = False
            previous_iter_score = 0
            last_fusion_frame = 9999
            frame_since_last_action = 0 

    print(f"End of instance {id_instance} game {current_game}, final score {handler.data['score']}")
    enregistrer_resultats('./data/game_results/resultats_recovered_dqn_discrete_agents.csv', agent_id, current_game, handler.data['score'], moves)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_q, pygame.K_ESCAPE]:
                    print(f"quit game {id_instance}")
                    pygame.quit()
                    sys.exit()

recovered_agent_games('test_recover', 'test', './data/agents/dqn_discrete_768c1a20-cedb-419c-9682-0f31cd0f9edd_after_game_75.h5', number_of_game=1)
