from game_classes import *

import sys
import numpy as np
import pygame
import pymunk
import random
import uuid

from config import Config


def random_game(id_instance, number_of_game=1):

    config = Config()
    id = str(uuid.uuid4())
    current_game = 1
    print(f"Starting random instance {id_instance}")
    last_action_time = pygame.time.get_ticks()

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

    # Main game loop
    game_over = False
    moves = 0
    fps_interval = config.screen.fps*2
    frame_since_last_action = 0

    while not game_over:
        current_time = pygame.time.get_ticks()
        # Take user input
        if pygame.event.peek():
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    print(f"quit game {id_instance}")
                    pygame.quit()
                    sys.exit()
        
        # Random agent
        if (frame_since_last_action >= fps_interval):
        # Générer et exécuter une action aléatoire
            random_x = random.randint(config.playground_left, config.playground_right)
            cloud.curr.set_x(random_x)
            particles.append(cloud.release(space))
            wait_for_next = config.screen.delay
            frame_since_last_action = 0
            moves += 1

        # Delay between fruit drop
        if wait_for_next > 1:
            wait_for_next -= 1
        if wait_for_next == 1:
            cloud.step()
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

        # Time step
        space.step(1/config.screen.fps)
        pygame.display.update()
        clock.tick(config.screen.fps)
        frame_since_last_action += 1

    # Reset game if number_of_game > 1
        if (game_over == True and current_game < number_of_game ):
            print(f"End of game {id_instance}, final score {handler.data['score']}")
            enregistrer_resultats('./data/game_results/resultats_random_agents.csv', id, current_game, handler.data['score'], moves)
            
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
            moves = 0


    print(f"End of game {id_instance}, final score {handler.data['score']}")
    enregistrer_resultats('./data/game_results/resultats_random_agents.csv', id, current_game, handler.data['score'], moves)

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
    

#random_game("test", 1)