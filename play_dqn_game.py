from dqn_agent import DQNAgent
from game_classes import *
from config import Config

import sys
import numpy as np
import pygame
import pymunk
import random


def dqn_games(id_instance, number_of_game=1):

    config = Config()
    board_width = config.playground_right - config.playground_left
    boarg_height = config.playground_bot - config.playground_top
    print(board_width, boarg_height)

    ### Init agent
    agent = DQNAgent((board_width, boarg_height,1), 2, 1)
    print(f"Agent {agent.id} initialisé")
    batch_size = 16

    ### Init game 
    current_game = 1
    print(f"Starting game {id_instance}, game {current_game}")

    last_action_time = pygame.time.get_ticks()
    action_interval = 1500 

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
    walls = [left, bottom, right]

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
    go_ham = False
    action_started = False
    initial_state = None
    next_state = None
    initial_score = 0
    reward = 0
    done = False
    moves = 0
    step_done = False
    training_freq = 32
    next_train_in = training_freq

    while not game_over:
        current_time = pygame.time.get_ticks()
        # Take user input
        if pygame.event.peek():
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    print(f"quit game {id_instance}")
                    pygame.quit()
                    sys.exit()
        
        if (len(agent.memory) > batch_size) and (next_train_in == 0):
            print(f"Agent {agent.id} from instance {id_instance} game number {current_game} is learning")
            agent.replay(batch_size)
            next_train_in = training_freq

        # Agent action
        if (current_time - last_action_time > action_interval) and (action_started==False) and (wait_for_next == 0):
            action_started = True
            initial_score = handler.data["score"]
            initial_state = get_board_state(particles, cloud)
            action = agent.act(initial_state)
            action_on_board = action*board_width + config.playground_left
            print(f'action: {action}, on board: {action_on_board}')
            cloud.curr.set_x(action_on_board)
            particles.append(cloud.release(space))
            step_done = False
            moves += 1
            last_action_time = current_time
            wait_for_next = config.screen.delay
            

        # Delay between fruit drop
        if wait_for_next > 1:
            wait_for_next -= 1
        if wait_for_next == 1:
            cloud.step()
            step_done = True
            wait_for_next -= 1

        if go_ham and wait_for_next == 0:
            particles.append(cloud.release(space))
            wait_for_next = config.screen.delay

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

        # Feedback
        if (current_time - last_action_time > action_interval) and (action_started) and (wait_for_next == 0) and (step_done):
            reward = 0
            next_state = get_board_state(particles, cloud)
            next_score = handler.data["score"]
            move_score = next_score - initial_score
            if move_score == 0:
                reward -= 1
            if game_over:
                done = True
                reward -= 10
            reward += move_score
            reward = np.array([reward])
            agent.remember(initial_state, action, reward, next_state, done)
            action_started = False
            next_train_in -= 1


        # Time step
        space.step(1/config.screen.fps)
        pygame.display.update()
        clock.tick(config.screen.fps)


        # Reset game if number_of_game > 1
        if (game_over == True and current_game < number_of_game ):
            print(f"End of game {id_instance}, final score {handler.data['score']}")
            enregistrer_resultats('./data/game_results/resultats_dqn_agents.csv', agent.id, current_game, handler.data['score'], moves)
            
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
            walls = [left, bottom, right]

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
            go_ham = False
            action_started = False
            initial_state = None
            next_state = None
            initial_score = 0
            reward = 0
            done = False
            moves = 0
            step_done = False


    print(f"End of game {id_instance}, final score {handler.data['score']}")
    enregistrer_resultats('./data/game_results/resultats_dqn_agents.csv', agent.id, current_game, handler.data['score'], moves)
    agent.model.save(f'./data/agents/dqn_{agent.id}.h5')

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

dqn_games('test_dqn', number_of_game=1)
