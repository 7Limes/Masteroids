import random
import pygame
from pygame import Vector2, Surface
import util
from globals import resource_manager, particle_effects, added_level_objects
from particle.particle import ParticleEffect
from objects.coin import Coin


ORBITER_RADIUS = 1.0
ORBITER_ACCEL = 10.0
ORBITER_VIEW_DISTANCE = 30.0


class Enemy(util.LevelObject):
    def __init__(self, position: Vector2, radius: float, velocity: Vector2, sprite: Surface, health: int):
        super().__init__(position, radius, velocity, sprite)
        self.health = health
        self.shake_cooldown = 0.0
    

    def destroy(self):
        global resource_manager, particle_effects
        self.queue_delete = True
        effect = ParticleEffect.primitive(20, self.position, 0, 360, 0, 200, 7, 1, 1, 0.2, 5, 2, (255, 50, 50), (255, 215, 0))
        particle_effects.append(effect)
        resource_manager.get_sound('explosion').play()

        coin = Coin(self.position, Vector2(random.uniform(-10, 10), random.uniform(-10, 10)))
        added_level_objects.append(coin)
    

    def damage(self):
        self.health -= 1
        if self.health <= 0:
            self.destroy()
        else:
            resource_manager.get_sound('hit').play()
            self.shake_cooldown = 0.1

    def draw(self, surf: Surface, view_pos: Vector2):
        offset = Vector2(0, 0)
        if self.shake_cooldown > 0:
            offset = Vector2(random.randint(-1, 1), random.randint(-1, 1))
        super().draw(surf, view_pos, offset)


class Orbiter(Enemy):
    def __init__(self, position: util.Vector2):
        enemy_sprite = Surface((24, 24), pygame.SRCALPHA)
        enemy_sprite.fill((255, 0, 0))
        super().__init__(position, ORBITER_RADIUS, Vector2(0, 0), enemy_sprite, 1)
    

    def update(self, delta: float, player_position: Vector2):
        if self.position.distance_to(player_position) < ORBITER_VIEW_DISTANCE:
            self.velocity += (player_position - self.position).normalize() * ORBITER_ACCEL * delta
        else:
            self.velocity.move_towards_ip((0, 0), 0.1)
        super().update(delta)