import math
import random
import pygame
from pygame import Vector2, Surface

import util
from particle.particle import ParticleEffect
from globals import resource_manager, particle_effects, added_level_objects
from objects.coin import Coin


class Asteroid(util.LevelObject):
    def __init__(self, position: Vector2, radius: float, velocity: Vector2, sprite: Surface=None):
        if sprite is None:
            sprite = resource_manager.get_image('asteroid')
        super().__init__(position, radius, velocity, sprite)
        
        self.health = math.floor(1.25 * math.sqrt(radius))
        self.shake_cooldown = 0.0
    

    def destroy(self):
        global resource_manager, particle_effects
        self.queue_delete = True
        sprites = resource_manager.get_full_spritesheet('fragments')
        particle_count = math.floor(8 * math.sqrt(self.radius) + 3)
        effect = ParticleEffect(particle_count, self.position, 0, 360, 0, 200, 3.5, 1, 2, 0.2, sprites)
        particle_effects.append(effect)
        resource_manager.get_sound('explosion').play()


    def damage(self):
        self.health -= 1
        if self.health <= 0:
            self.destroy()
        else:
            resource_manager.get_sound('hit').play()
            self.shake_cooldown = 0.1

    
    def update(self, delta: float) -> bool:
        super().update(delta)
        self.shake_cooldown = util.move_toward(self.shake_cooldown, 0, delta)


    def draw(self, surf: Surface, view_pos: Vector2):
        offset = Vector2(0, 0)
        if self.shake_cooldown > 0:
            offset = Vector2(random.randint(-1, 1), random.randint(-1, 1))
        super().draw(surf, view_pos, offset)
    

class CoinAsteroid(Asteroid):
    def __init__(self, position: Vector2, radius: float, velocity: Vector2):
        coin_asteroid_sprite = resource_manager.get_image('dest_asteroid')
        super().__init__(position, radius, velocity, coin_asteroid_sprite)
    

    def destroy(self):
        global added_level_objects
        super().destroy()
        amount_coins = math.floor(2 * math.sqrt(self.radius) + random.randint(-1, 1))
        for _ in range(amount_coins):
            coin_position: Vector2 = self.position + Vector2.from_polar((random.uniform(0, self.radius), random.uniform(0, 360)))
            coin_velocity = (coin_position - self.position).normalize() * 15
            coin = Coin(coin_position, coin_velocity)
            added_level_objects.append(coin)

