import numpy as np
import pygame
import pymunk
import csv
from config import Config

# Config
config = Config()
rng = np.random.default_rng()

class Particle(pymunk.Circle):
    def __init__(self, pos, n, space):
        self.n = n % 11
        super().__init__(body=pymunk.Body(body_type=pymunk.Body.DYNAMIC), radius= config[self.n, "radius"])
        self.body.position = tuple(pos)
        self.density = config.physics.density
        self.elasticity = config.physics.elasticity
        self.collision_type = 1
        self.friction = 0.4
        self.has_collided = False
        self.alive = True
        space.add(self.body, self)

    def draw(self, screen):
        # if self.alive:
        #     sprite = pygame.transform.rotate(config[self.n, "blit"].copy(), -self.body.angle * 180/np.pi)
        #     screen.blit(sprite, self.sprite_pos(sprite))
        if self.alive:
            sprite = config[self.n, "blit"].copy()  # Utilisez directement le sprite sans rotation
            screen.blit(sprite, self.sprite_pos(sprite))

    def kill(self, space):
        space.remove(self.body, self)
        self.alive = False

    @property
    def pos(self):
        return np.array(self.body.position)

    @property
    def radius(self):
        return config[self.n, "radius"]

    @property
    def pos_radius(self):
        return (self.pos, self.radius )

    def position_in_image(self):
        x = self.pos[0] - config.pad.left
        y = self.pos[1] - config.pad.top
        return (x, y)

    def sprite_pos(self, sprite):
        x, y = self.body.position
        w, h = sprite.get_size()
        a, b = self.sprite_offset
        return x - w / 2 + a, y - h / 2 + b

    @property
    def sprite_offset(self):
        ang = self.body.angle
        mat = np.array([
            [np.cos(ang), -np.sin(ang)],
            [np.sin(ang), np.cos(ang)],
        ])
        arr = np.array(config[self.n, "offset"])
        return mat @ arr


class PreParticle:
    def __init__(self):
        self.x = config.screen.width // 2
        self.n = rng.integers(0, 5)
        self.radius = config[self.n, "radius"]
        self.sprite = config[self.n, "blit"]
        self.fruit_name = config.fruit_names[self.n]
    def draw(self, screen, wait):
        screen.blit(config.cloud_blit, (self.x, 8))
        if not wait:
            pygame.draw.line(
                screen,
                color=config.screen.white,
                start_pos=(self.x, config.pad.line_top),
                end_pos=(self.x, config.pad.line_bot),
                width=2,
            )
            screen.blit(self.sprite, self.sprite_pos)

    def pre_draw(self, screen):
        screen.blit(self.sprite, self._sprite_pos((1084, 185)))

    @property
    def sprite_pos(self):
        return self._sprite_pos((self.x, config.pad.top))
    
    @property
    def sprite_pos(self):
        return self._sprite_pos((self.x, config.pad.top))

    def _sprite_pos(self, pos):
        x, y = pos
        w, h = self.sprite.get_size()
        a, b = config[self.n, "offset"]
        return x - w / 2 + a, y - h / 2 + b

    def set_x(self, x):
        left_lim = config.pad.left + self.radius
        right_lim = config.pad.right - self.radius
        self.x = np.clip(x, left_lim, right_lim)

    def release(self, space):
        return Particle((self.x, config.pad.top), self.n, space)


class Cloud:
    def __init__(self):
        self.curr = PreParticle()
        self.next = PreParticle()

    def draw(self, screen, wait):
        self.curr.draw(screen, wait)
        self.next.pre_draw(screen)

    def release(self, space):
        return self.curr.release(space)

    def step(self):
        self.curr = self.next
        self.next = PreParticle()


class Wall(pymunk.Segment):
    def __init__(self, a, b, space):
        super().__init__(body=pymunk.Body(body_type=pymunk.Body.STATIC), a=a, b=b, radius=2)
        self.friction = 10
        space.add(self.body, self)


def resolve_collision(particle1, particle2, space, particles):
    distance = np.linalg.norm(particle1.pos - particle2.pos)
    if distance < 2 * particle1.radius:
        particle1.kill(space)
        particle2.kill(space)
        new_particle = Particle(np.mean([particle1.pos, particle2.pos], axis=0), particle1.n + 1, space)
        for p in particles:
            if p.alive:
                vector = p.pos - new_particle.pos
                distance = np.linalg.norm(vector)
                if distance < new_particle.radius + p.radius:
                    impulse = config.physics.impulse * vector / (distance ** 2)
                    p.body.apply_impulse_at_local_point(tuple(impulse))
        return new_particle
    return None

def collide(arbiter, space, data):
    particle1, particle2 = arbiter.shapes
    alive = particle1.alive and particle2.alive
    same = particle1.n == particle2.n
    particle1.has_collided = not same
    particle2.has_collided = not same
    if same and alive:
        new_particle = resolve_collision(particle1, particle2, space, data["particles"])
        data["particles"].append(new_particle)
        data["score"] += config[particle1.n, "points"]
    return not same and alive

def get_board_state(particles, cloud):
    current_fruit = {"n":cloud.curr.n, "name":cloud.curr.fruit_name, "radius": cloud.curr.radius}
    next_fruit = {"n":cloud.next.n, "name":cloud.next.fruit_name, "radius": cloud.next.radius}
    width = config.pad.right - config.pad.left
    height = config.pad.bot - config.pad.top
    image = np.zeros((width, height, 1))
    for particle in particles:
        if particle.alive:
            x, y = particle.position_in_image()
            x = round(x)
            y = round(y)
            image[x, y, 0] = particle.radius
    current_and_next_fruit = np.array([current_fruit["radius"], next_fruit["radius"]])
    return [np.expand_dims(image, axis=0), np.array([current_and_next_fruit])]

def get_board_state_resized(particles, cloud, new_width, new_height):
    current_fruit = {"n":cloud.curr.n, "name":cloud.curr.fruit_name, "radius": cloud.curr.radius}
    next_fruit = {"n":cloud.next.n, "name":cloud.next.fruit_name, "radius": cloud.next.radius}
    width = config.pad.right - config.pad.left
    height = config.pad.bot - config.pad.top
    scale_x = new_width / width
    scale_y = new_height / height
    resized_image = np.zeros((new_width, new_height, 1))
    for particle in particles:
        if particle.alive:
            x, y = particle.position_in_image()
            new_x = round(x * scale_x)
            new_y = round(y * scale_y)
            new_x = min(new_x, new_width - 1)
            new_y = min(new_y, new_height - 1)

            resized_image[new_x, new_y, 0] =  particle.radius
    current_and_next_fruit = np.array([current_fruit["radius"], next_fruit["radius"]])
    return [np.expand_dims(resized_image, axis=0), np.array([current_and_next_fruit])]

def enregistrer_resultats(nom_fichier, agent_id, numero_partie, score_final, coups_joues):
    with open(nom_fichier, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([agent_id, numero_partie, score_final, coups_joues])
