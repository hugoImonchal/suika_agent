from game_classes import *

import sys
import numpy as np
import pygame
import pymunk
import random

from config import Config


def lancer_jeu(id_instance, number_of_game=1):
    current_game = 1
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
    go_ham = False
    while not game_over:
        # Take user input
        if pygame.event.peek():
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and wait_for_next == 0:
                    particles.append(cloud.release(space))
                    wait_for_next = config.screen.delay
                    print(f"Clic à la position {event.pos}")
                elif (event.type == pygame.KEYDOWN and event.key == pygame.K_r):
                    random_x = random.randint(config.playground_left, config.playground_right)
                    print(f"state of the board {[particle.pos_radius for particle in particles if particle.alive]}")
                    cloud.curr.set_x(random_x)
                    particles.append(cloud.release(space))
                    wait_for_next = config.screen.delay
                    print(f"Particule pos x {random_x}")
                    # clic_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (random_x, 100), 'button': 1})
                    # pygame.event.post(clic_event)
                    # print(f"Posted a click on random position {(random_x, 100)}")
                

        cloud.curr.set_x(pygame.mouse.get_pos()[0])

        # Delay between fruit drop
        if wait_for_next > 1:
            wait_for_next -= 1
        if wait_for_next == 1:
            cloud.step()
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
        if len(particles) > 5:
            label = overfont.render("Game Over!", 1, (0, 0, 0))
            screen.blit(label, (30, 160))
            game_over = True

        label = scorefont.render(f"Score: {handler.data['score']}", 1, (0, 0, 0))
        screen.blit(label, (10, 10))

        # Time step
        space.step(1/config.screen.fps)
        pygame.display.update()
        clock.tick(config.screen.fps)

        if (game_over == True and current_game < number_of_game ):
            current_game += 1
            print('reset')
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

            # Main game loop
            game_over = False
            go_ham = False
            


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_q, pygame.K_ESCAPE]:
                    print("exit")
                    pygame.quit()
                    sys.exit()
                    

lancer_jeu("test", number_of_game=1)