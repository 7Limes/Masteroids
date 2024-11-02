import math
import random
import pygame
from pygame import Vector2, Surface
import util
from particle.particle import ParticleEffect
from globals import resource_manager, particle_effects

class Asteroid(util.DynamicCollisionCircle):
    def __init__(self, position: Vector2, radius: float, velocity: Vector2, mass: float):
        super().__init__(position, radius, velocity, mass)
        self.image_name = 'asteroid'

        self.destroyed = False
        self.health = math.floor(1.25 * math.sqrt(radius))
        self.shake_cooldown = 0.0
    

    def damage(self):
        self.health -= 1
        if self.health <= 0:
            self.destroyed = True
            sprites = resource_manager.get_full_spritesheet('fragments')
            particle_count = math.floor(8 * math.sqrt(self.radius) + 3)
            effect = ParticleEffect(particle_count, self.position, 0, 360, 0, 200, 3.5, 1, 2, 0.2, sprites)
            particle_effects.append(effect)
            resource_manager.get_sound('explosion').play()
        else:
            resource_manager.get_sound('hit').play()
            self.shake_cooldown = 0.1

    
    def update(self, delta: float):
        super().update(delta)
        self.shake_cooldown = util.move_toward(self.shake_cooldown, 0, delta)
        return self.destroyed


    def draw(self, surf: Surface, view_pos: Vector2):
        asteroid_sprite = resource_manager.get_image(self.image_name)

        scaled_sprite_size = self.radius * 2 * util.RENDER_SCALE
        scaled_sprite_size_vec = Vector2(scaled_sprite_size, scaled_sprite_size)
        scaled_asteroid_sprite = pygame.transform.scale(asteroid_sprite, Vector2(scaled_sprite_size, scaled_sprite_size))

        screen_coord = self.get_screen_coord(surf, view_pos)
        if self.shake_cooldown > 0:
            screen_coord += Vector2(random.randint(-1, 1), random.randint(-1, 1))
        surf.blit(scaled_asteroid_sprite, screen_coord - scaled_sprite_size_vec / 2.0)
        # super().draw(surf, view_pos)  # draw debug hitbox
    

class DestructibleAsteroid(Asteroid):
    def __init__(self, position: Vector2, radius: float, velocity: Vector2, mass: float):
        super().__init__(position, radius, velocity, mass)
        self.image_name = 'dest_asteroid'